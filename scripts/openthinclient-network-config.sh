#!/bin/bash -eux
# Purpose:      configure basic network settings
#------------------------------------------------------------------------------

# Disable Predictable Network Interface Names (force eth0 naming)
ln -sf /dev/null /etc/udev/rules.d/80-net-setup-link.rules

# Write minimal network interfaces config
cat <<'EOF' > /etc/network/interfaces
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto eth0
iface eth0 inet dhcp
pre-up sleep 2
EOF
