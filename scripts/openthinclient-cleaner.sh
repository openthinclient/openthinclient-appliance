#!/bin/bash
# Filename:     openthinclient-cleaner.sh
# Purpose:      cleanup openthinclient and system stuff before shrinking
#------------------------------------------------------------------------------

DISK_USAGE_BEFORE_CLEANUP=$(df -h)

echo "==> Cleaning up leftover dhcp leases"
if [ -d "/var/lib/dhcp" ]; then
    rm /var/lib/dhcp/*
fi

echo "==> Cleaning up tmp"
rm -rf /tmp/*


echo "==> Stopping the openthinclient server before cleaning up"
/etc/init.d/openthinclient stop

echo "==> Making sure the openthinclient server is stopped"
/etc/init.d/openthinclient status

# remove lock and log files
find /opt/openthinclient/ | grep '\.db\.lock' | xargs rm
find /opt/openthinclient/ | grep '\.log' | xargs rm

# remove nfs db
rm /opt/openthinclient/server/default/data/nfs-paths.db*

# remove homes
rm -rf 	/opt/openthinclient/server/default/data/nfs/home/*

# remove jboss stuff
rm -rf /opt/openthinclient/server/default/data/tx-object-store 
rm -rf /opt/openthinclient/server/default/data/hypersonic
rm -rf /opt/openthinclient/server/default/data/xmbean-attrs
rm -f /opt/openthinclient/server/default/data/jboss.identity

# delete ldap backups
find /var/backups/openthinclient/ -name "*\.ldiff\.*" -type f | xargs rm

# cleanup teamviewer config
echo "==> Cleaning up teamviewer global configuration"
if [ -f "/opt/teamviewer9/config/global.conf" ]; then
    rm /opt/teamviewer9/config/global.conf
fi

#rm /opt/teamviewer9/config/global.conf
rm /opt/teamviewer9/config/openthinclient/client.conf
# /opt/teamviewer9/tv_bin/teamviewerd -d


# Cleaning up oracle-jdk8-installer cache dir
echo "==> Cleaning up /var/cache/oracle-jdk8-installer folder"
if [ -d "/var/cache/oracle-jdk8-installer/" ]; then
    rm -rf /var/cache/oracle-jdk8-installer/*
fi

#------------------------------------------------------------------------------
# general

echo "==> remove udev network rules to cleanup old interfaces"
if [ -f "/etc/udev/rules.d/70-persistent-net.rules" ]; then
    rm /etc/udev/rules.d/70-persistent-net.rules
fi

echo "==> Cleanup apt cache"
apt-get -y autoremove --purge
apt-get -y clean
apt-get -y autoclean


# clean history
echo "==> Clean openthinclient .bash_history file if exists"
if [ -f "/home/openthinclient/.bash_history" ]; then
    rm /home/openthinclient/.bash_history
fi

# clean root history
echo "==> Clean /root/.bash_history file if exists"
if [ -f "/root/.bash_history" ]; then
	rm /root/.bash_history
fi

# clean logs
for i in `find /var/log/ -name "*log" -type f`
do
	>$i
done

find /var/log/ -name "*\.log\.*" -type f | xargs rm
find /var/log/ -name "*\.0" -type f | xargs rm
find /var/log/ -name "*\.[0-9]*\.gz" -type f | xargs rm


echo "==> Disk usage before cleanup"
echo ${DISK_USAGE_BEFORE_CLEANUP}

echo "==> Disk usage after cleanup"
df -h

## zero out swap and mkswap again
#swapSpace=$(swapon -s | tail -n 1 | awk '{print $1}')
#echo $swapSpace | grep -qv Filename && (
#    swapoff $swapSpace
#    dd if=/dev/zero of=$swapSpace
#    mkswap -f $swapSpace
#)
#
## shrink root fs
## are we inside a vmware guest-host?
#which vmware-toolbox-cmd &> /dev/null
#if [ $? -eq 0 ]; then
#    echo "It seems we're inside an VMware-Guest. Will now use vmware-tools to shrink harddisc."
#    vmware-toolbox-cmd disk shrink /boot
#else 
#    echo "No VMware tools could be found. I guess we're inside some other type of virtual host."
#    echo "Do you want to reboot the system and fill your unused harddisc space with zeros?"
#    echo "You'll need to do so if you want to shrink your HD. [y/N]"
#    read goon
#    if [ "$goon" = "y" ]; then
#	grub-reboot shrink-disc-$(uname -r)
#	reboot -f
#    fi
#fi

