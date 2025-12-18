#!/bin/bash -eux
# Purpose:      configure basic network settings
#------------------------------------------------------------------------------

# Disable Predictable Network Interface Names (force eth0 naming)
ln -sf /dev/null /etc/udev/rules.d/80-net-setup-link.rules

# Write minimal network interfaces config
cat <<'EOF' > /etc/network/interfaces

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

EOF
