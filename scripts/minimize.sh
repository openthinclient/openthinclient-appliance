#!/bin/sh -eux
# Filename:     minimize.sh
# Purpose:      generate zero space to prepare VM for disk shrinking
#------------------------------------------------------------------------------

DISK_USAGE_BEFORE_CLEANUP=$(df -h)

swapuuid="`/sbin/blkid -o value -l -s UUID -t TYPE=swap`";

if [ "x${swapuuid}" != "x" ]; then
    # Whiteout the swap partition to reduce box size
    # Swap is disabled till reboot
    swappart="`readlink -f /dev/disk/by-uuid/$swapuuid`";
    /sbin/swapoff "$swappart";
    dd if=/dev/zero of="$swappart" bs=1M || echo "dd exit code $? is suppressed";
    /sbin/mkswap -U "$swapuuid" "$swappart";
fi

dd if=/dev/zero of=/EMPTY bs=1M || echo "dd exit code $? is suppressed";
rm -f /EMPTY;
# Block until the empty file has been removed, otherwise, Packer
# will try to kill the box while the disk is still full and that's bad
sync;

echo "==> Disk usage before cleanup"
echo ${DISK_USAGE_BEFORE_CLEANUP}

echo "==> Disk usage after cleanup"
df -h