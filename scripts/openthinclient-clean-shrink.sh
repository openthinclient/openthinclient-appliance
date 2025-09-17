#!/bin/bash -eux
# Purpose:      Cleanup openthinclient + system, then zero-fill free space for shrinking
#------------------------------------------------------------------------------

export DEBIAN_FRONTEND="noninteractive"

# --- Config -------------------------------------------------------------------
OTC_INSTALL_PATH="/opt/otc-manager/"
OTC_INSTALL_HOME="/home/openthinclient/otc-manager-home/"
OTC_SERVICE="openthinclient-manager"
OTC_CACHE_DIR="${OTC_INSTALL_HOME}nfs/root/var/cache/archives/"
OTC_LOG_DIR="${OTC_INSTALL_HOME}logs/"
OTC_BACKUPS_DIR="/var/backups/openthinclient/"
JDK_CACHE_DIR="/var/cache/oracle-jdk8-installer/"
DHCP_DIR="/var/lib/dhcp"
TMP_DIR="/tmp"
UDEV_RULES="/etc/udev/rules.d/70-persistent-net.rules"
OTC_BASH_HISTORY="/home/openthinclient/.bash_history"
ROOT_BASH_HISTORY="/root/.bash_history"
LOG_DIR="/var/log"

# --- Helpers ------------------------------------------------------------------
log() { echo "==> $*"; }

cleanup_directory() {
  local dir=$1
  if [[ -d "$dir" ]]; then
    # Remove normal + hidden entries (but not . or ..)
    rm -rf "${dir:?}/"* 2>/dev/null || true
    rm -rf "${dir:?}/".* 2>/dev/null || true
    log "Cleaned up ${dir}"
  fi
}

maybe_cmd() { command -v "$1" >/dev/null 2>&1; }

# --- Pre-flight ---------------------------------------------------------------
if [[ $EUID -ne 0 ]]; then
  echo "Please run as root." >&2
  exit 1
fi

log "Disk usage before cleanup"
df -h

# --- Stop service -------------------------------------------------------------
if systemctl list-unit-files | grep -q "^${OTC_SERVICE}\.service"; then
  if systemctl is-active --quiet "${OTC_SERVICE}"; then
    log "Stopping ${OTC_SERVICE} before cleaning up"
    systemctl stop "${OTC_SERVICE}"
    sleep 5
    if systemctl is-active --quiet "${OTC_SERVICE}"; then
      log "WARNING: ${OTC_SERVICE} still active"; systemctl status "${OTC_SERVICE}" || true
    else
      log "${OTC_SERVICE} is stopped"
    fi
  else
    log "${OTC_SERVICE} is not active"
  fi
else
  log "Service ${OTC_SERVICE} not found (skipping)"
fi

# --- openthinclient cleanup ---------------------------------------------------
if [[ -d "${OTC_INSTALL_HOME}" ]]; then
  find "${OTC_CACHE_DIR}" -type f -name "*.deb" -exec rm -f {} + 2>/dev/null || true
  cleanup_directory "${OTC_CACHE_DIR}1"
  cleanup_directory "${OTC_CACHE_DIR}2"
  cleanup_directory "${OTC_INSTALL_HOME}nfs/home"

  if [[ -x "${OTC_INSTALL_PATH}bin/managerctl" ]]; then
    log "Removing openthinclient-Management server id"
    "${OTC_INSTALL_PATH}bin/managerctl" rm-server-id --home "${OTC_INSTALL_HOME}" || true
  fi

  if [[ -f "${OTC_INSTALL_HOME}directory/service.xml" ]]; then
    sed -i 's#<accessControlEnabled>true</accessControlEnabled>#<accessControlEnabled>false</accessControlEnabled>#' \
      "${OTC_INSTALL_HOME}directory/service.xml" || true
    log "Patched accessControlEnabled=false in service.xml (if present)"
  fi

  cleanup_directory "${OTC_LOG_DIR}"
fi

if [[ -d "${OTC_BACKUPS_DIR}" ]]; then
  find "${OTC_BACKUPS_DIR}" -type f -name "*.ldiff.*" -exec rm -f {} + || true
  log "Deleted LDAP backups in ${OTC_BACKUPS_DIR}"
fi

# --- System cleanup -----------------------------------------------------------
cleanup_directory "${JDK_CACHE_DIR}"
cleanup_directory "${DHCP_DIR}"
cleanup_directory "${TMP_DIR}"

if [[ -f "${UDEV_RULES}" ]]; then
  rm -f "${UDEV_RULES}"
  log "Removed udev network rules ${UDEV_RULES}"
fi

[[ -f "${OTC_BASH_HISTORY}" ]] && rm -f "${OTC_BASH_HISTORY}" && log "Deleted openthinclient .bash_history"
[[ -f "${ROOT_BASH_HISTORY}" ]] && rm -f "${ROOT_BASH_HISTORY}" && log "Deleted root .bash_history"

if maybe_cmd apt-get; then
  log "Running apt autoremove/autoclean/clean"
  apt-get -y autoremove --purge || true
  apt-get -y autoclean || true
  apt-get -y clean || true
fi

log "Cleaning logs under ${LOG_DIR}"
# Remove rotated/compressed logs
find "${LOG_DIR}" -type f -name "*.log.*" -delete || true
find "${LOG_DIR}" -type f -name "*.0" -delete || true
find "${LOG_DIR}" -type f -regextype posix-extended -regex '.*\.[0-9]+\.gz$' -delete || true
# Truncate current logs (keep files/permissions)
find "${LOG_DIR}" -type f -name "*.log" -exec sh -c ': > "$1"' _ {} \; 2>/dev/null || true
# Journal cleanup (if systemd)
if maybe_cmd journalctl; then
  journalctl --rotate || true
  journalctl --vacuum-time=1s || true
fi

log "Disk usage after cleanup"
df -h

# --- Minimize (zero-fill) -----------------------------------------------------
log "Starting zero-fill minimize step"

# Prefer handling both swap partition and swap file
# 1) Try partition by UUID
SWAPUUID="$(blkid -o value -l -s UUID -t TYPE=swap || true)"
SWAPPART=""
if [[ -n "${SWAPUUID:-}" ]]; then
  SWAPPART="$(readlink -f "/dev/disk/by-uuid/${SWAPUUID}" || true)"
fi

# 2) Detect swap files from /proc/swaps (skip partitions already covered)
SWAPFILES=()
while IFS= read -r line; do
  path=$(awk '{print $1}' <<<"$line")
  [[ -f "$path" ]] && SWAPFILES+=("$path")
done < <(tail -n +2 /proc/swaps 2>/dev/null || true)

# Partition case
if [[ -n "${SWAPPART}" && -b "${SWAPPART}" ]]; then
  log "Disabling swap on ${SWAPPART}"
  swapoff "${SWAPPART}" || true
  log "Zero-filling swap partition..."
  dd if=/dev/zero of="${SWAPPART}" bs=1M status=none || echo "dd exit code $? is suppressed"
  log "Recreating swap with original UUID"
  mkswap -U "${SWAPUUID}" "${SWAPPART}" >/dev/null || true
fi

# Swapfile case(s)
for sf in "${SWAPFILES[@]}"; do
  log "Disabling swap file ${sf}"
  swapoff "${sf}" || true
  # Try to zero the file contents without changing size
  if command -v fallocate >/dev/null 2>&1; then
    # fallocate --collapse-range is not portable; use dd overwrite
    dd if=/dev/zero of="${sf}" bs=1M conv=notrunc status=none || echo "dd exit code $? is suppressed"
  else
    dd if=/dev/zero of="${sf}" bs=1M conv=notrunc status=none || echo "dd exit code $? is suppressed"
  fi
  mkswap "${sf}" >/dev/null || true
done

# Fill free space on root
log "Zero-filling free space with /EMPTY (this can take a while)..."
dd if=/dev/zero of=/EMPTY bs=1M status=none || echo "dd exit code $? is suppressed"
rm -f /EMPTY
sync
log "Minimize step complete"

log "All done. You can now shut down the VM and shrink/compact the disk."
