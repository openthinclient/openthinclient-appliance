#!/bin/bash -eux
# Filename:     motd.sh
# Purpose:      adapt message of the day to show some useful information
#------------------------------------------------------------------------------

echo "==> Customizing message of the day"
MOTD_FILE=/etc/motd
BANNER_WIDTH=64
#PLATFORM_RELEASE=$(lsb_release -sd)
PLATFORM_MSG=$(printf 'openthinclient %s' "$OTC_APPLIANCE_VERSION")
BUILT_MSG=$(printf 'built %s' $(date +%Y-%m-%d))

printf '%0.1s' "-"{1..64} > ${MOTD_FILE}
printf '\n' >> ${MOTD_FILE}
printf '%2s%-30s%30s\n' " " "${PLATFORM_MSG}" "${BUILT_MSG}" >> ${MOTD_FILE}
printf '%0.1s' "-"{1..64} >> ${MOTD_FILE}
printf '\n' >> ${MOTD_FILE}
