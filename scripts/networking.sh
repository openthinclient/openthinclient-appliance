#!/usr/bin/env bash -eux
# Filename:     networking.sh
# Purpose:      configure basic network settings
#-----------------------

# disable Predictable Network Interface Names and go back to basic eth0
ln -s /dev/null /etc/udev/rules.d/80-net-setup-link.rules

echo '# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
#auto lo
#iface lo inet loopback

# The primary network interface
#auto eth0
#iface eth0 inet dhcp
#pre-up sleep 2' > /etc/network/interfaces
