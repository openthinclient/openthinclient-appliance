#!/bin/bash -eux
# Filename:     minimize.sh
# Purpose:      generate zero space to prepare VM for disk shrinking
#------------------------------------------------------------------------------

swapuuid="$(/sbin/blkid -o value -l -s UUID -t TYPE=swap)";

if [ -n "$swapuuid" ]; then
    # Whiteout the swap partition to reduce box size
    # Swap is disabled till reboot
    swappart="$(readlink -f /dev/disk/by-uuid/"$swapuuid")";
    /sbin/swapoff "$swappart";
    dd if=/dev/zero of="$swappart" bs=1M || echo "dd exit code $? is suppressed";
    /sbin/mkswap -U "$swapuuid" "$swappart";
fi

dd if=/dev/zero of=/EMPTY bs=1M || echo "dd exit code $? is suppressed";
rm -f /EMPTY;
# Block until the empty file has been removed, otherwise, Packer
# will try to kill the box while the disk is still full and that's bad
sync;
