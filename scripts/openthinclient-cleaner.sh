#!/bin/bash
# Filename:     openthinclient-cleaner.sh
# Purpose:      cleanup openthinclient and system stuff before shrinking
#------------------------------------------------------------------------------

DISK_USAGE_BEFORE_CLEANUP=$(df -h)

# Please sync these with the unattended linux-varfile
OTC_INSTALL_PATH=/opt/otc-manager/

# location of the home working directory
OTC_INSTALL_HOME=/home/openthinclient/otc-manager-home/

#------------------------------------------------------------------------------
# openthinclient specific cleanup

if [ -f "/etc/systemd/system/openthinclient-manager.service" ]; then
    echo "==> Stopping the openthinclient server before cleaning up"
    service openthinclient-manager stop

    # wait for shutdown
    sleep 60
    echo "==> Making sure the openthinclient server is stopped"
    service openthinclient-manager status
fi

if [ -d "/home/openthinclient/otc-manager-home/" ]; then

    # remove all downloaded openthinclient dpkg packages
    find  /home/openthinclient/otc-manager-home/nfs/root/var/cache/archives/ -name "*.deb" -exec rm {} \;

    # remove cache files
    rm -rf /home/openthinclient/otc-manager-home/nfs/root/var/cache/archives/1/*
    rm -rf /home/openthinclient/otc-manager-home/nfs/root/var/cache/archives/2/*

    # remove homes
    rm -rf /home/openthinclient/otc-manager-home/nfs/home/*

    # Remove unique server id
    ${OTC_INSTALL_PATH}bin/managerctl rm-server-id --home ${OTC_INSTALL_HOME}

    # disable accessControlEnabledto to generate custom password on next restart
    sed -i 's#<accessControlEnabled>true</accessControlEnabled>#<accessControlEnabled>false</accessControlEnabled>#' ${OTC_INSTALL_HOME}directory/service.xml

    # remove old logfiles from manager home
    rm -rf /home/openthinclient/otc-manager-home/logs/*

    # Remove unique server id
    ${OTC_INSTALL_PATH}bin/managerctl rm-server-id --home ${OTC_INSTALL_HOME}
fi

# delete ldap backups
if [ -d "/var/backups/openthinclient/ " ]; then
    find /var/backups/openthinclient/ -print -name "*\.ldiff\.*" -type f -exec rm -rf {} \;
fi

# Cleaning up oracle-jdk8-installer cache dir
echo "==> Cleaning up /var/cache/oracle-jdk8-installer folder"
if [ -d "/var/cache/oracle-jdk8-installer/" ]; then
    rm -rf /var/cache/oracle-jdk8-installer/*
fi

#------------------------------------------------------------------------------
# general

echo "==> Cleaning up leftover dhcp leases"
if [ -d "/var/lib/dhcp" ]; then
    rm /var/lib/dhcp/*
fi

echo "==> Cleaning up tmp"
rm -rf /tmp/*

echo "==> Remove udev network rules to cleanup old interfaces"
if [ -f "/etc/udev/rules.d/70-persistent-net.rules" ]; then
    rm /etc/udev/rules.d/70-persistent-net.rules
fi

echo "==> Removing pipewire and xdg-desktop-portal"
apt-get purge -y pipewire 
apt-get purge -y xdg-desktop-portal

echo "==> Cleanup apt cache"
apt-get -y autoremove --purge
apt-get -y clean
apt-get -y autoclean

# clean history
echo "==> Delete openthinclient .bash_history file if exists"
if [ -f "/home/openthinclient/.bash_history" ]; then
    rm /home/openthinclient/.bash_history
fi

# clean root history
echo "==> Clean /root/.bash_history file if exists"
if [ -f "/root/.bash_history" ]; then
	rm /root/.bash_history
fi

echo "==> Cleanup /var/log/"
find /var/log/ -name "*\.log\.*" -type f -delete
find /var/log/ -name "*\.0" -type f -delete
find /var/log/ -name "*\.[0-9]*\.gz" -type f -delete

echo "==> Disk usage before cleanup"
echo "${DISK_USAGE_BEFORE_CLEANUP}"

echo "==> Disk usage after cleanup"
df -h