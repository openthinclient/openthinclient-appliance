#!/bin/bash
# Filename:     openthinclient-cleaner.sh
# Purpose:      cleanup openthinclient and system stuff before shrinking
#------------------------------------------------------------------------------

DISK_USAGE_BEFORE_CLEANUP=$(df -h)
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
LOG_DIR="/var/log/"

log_message() {
    echo "==> $1"
}

cleanup_directory() {
    local dir=$1
    if [ -d "$dir" ]; then
        rm -rf "${dir:?}"/*
        log_message "Cleaned up ${dir}"
    fi
}

stop_service() {
    local service=$1
    if systemctl is-active --quiet "${service}"; then
        log_message "Stopping the ${service} server before cleaning up"
        systemctl stop "${service}"
        sleep 30
        log_message "Making sure the ${service} server is stopped"
        systemctl status "${service}"
    else
        log_message "${service} is not active or not found"
    fi
}

cleanup_apt() {
    apt-get -y autoremove --purge
    apt-get -y autoclean
    apt-get -y clean
}

cleanup_logs() {
    find ${LOG_DIR} -name "*\.log\.*" -type f -delete
    find ${LOG_DIR} -name "*\.0" -type f -delete
    find ${LOG_DIR} -name "*\.[0-9]*\.gz" -type f -delete
    log_message "Cleaned up logs in ${LOG_DIR}"
}

log_message "Disk usage before cleanup"
echo "${DISK_USAGE_BEFORE_CLEANUP}"

stop_service ${OTC_SERVICE}

if [ -d "${OTC_INSTALL_HOME}" ]; then
    find ${OTC_CACHE_DIR} -name "*.deb" -exec rm {} \;
    cleanup_directory "${OTC_CACHE_DIR}1"
    cleanup_directory "${OTC_CACHE_DIR}2"
    cleanup_directory "${OTC_INSTALL_HOME}nfs/home"
    ${OTC_INSTALL_PATH}bin/managerctl rm-server-id --home ${OTC_INSTALL_HOME}
    sed -i 's#<accessControlEnabled>true</accessControlEnabled>#<accessControlEnabled>false</accessControlEnabled>#' ${OTC_INSTALL_HOME}directory/service.xml
    cleanup_directory "${OTC_LOG_DIR}"
fi

if [ -d "${OTC_BACKUPS_DIR}" ]; then
    find ${OTC_BACKUPS_DIR} -name "*.ldiff.*" -type f -exec rm -rf {} \;
    log_message "Deleted LDAP backups in ${OTC_BACKUPS_DIR}"
fi

cleanup_directory "${JDK_CACHE_DIR}"
cleanup_directory "${DHCP_DIR}"
cleanup_directory "${TMP_DIR}"

if [ -f "${UDEV_RULES}" ]; then
    rm ${UDEV_RULES}
    log_message "Removed udev network rules ${UDEV_RULES}"
fi

if [ -f "${OTC_BASH_HISTORY}" ]; then
    rm ${OTC_BASH_HISTORY}
    log_message "Deleted openthinclient .bash_history"
fi

if [ -f "${ROOT_BASH_HISTORY}" ]; then
    rm ${ROOT_BASH_HISTORY}
    log_message "Deleted root .bash_history"
fi

cleanup_logs

log_message "Disk usage after cleanup"
df -h
