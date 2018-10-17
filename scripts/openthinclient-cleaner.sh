#!/bin/bash
# Filename:     openthinclient-cleaner.sh
# Purpose:      cleanup openthinclient and system stuff before shrinking
#------------------------------------------------------------------------------

DISK_USAGE_BEFORE_CLEANUP=$(df -h)

# Please sync these with the unattended linux-varfile
OTC_INSTALL_PATH=/opt/otc-manager/
#echo ${OTC_INSTALL_PATH}
#echo $OTC_INSTALL_PATH

# location of the home working directory
OTC_INSTALL_HOME=/home/openthinclient/otc-manager-home/

#------------------------------------------------------------------------------
# openthinclient specific cleanup

if [ -f "/etc/init.d/openthinclient-manager" ]; then
    echo "==> Stopping the openthinclient server before cleaning up"
    /etc/init.d/openthinclient-manager stop

    # wait for shutdown
    while lsof -i -n -P | grep 8080 &>/dev/null; do
	    sleep 1
	    echo "Waiting for shutdown...."
    done
    echo "==> Making sure the openthinclient server is stopped"
    /etc/init.d/openthinclient-manager status
fi

if [ -d "/home/openthinclient/otc-manager-home/" ]; then

    # remove all downloaded openthinclient dpkg packages
    find  /home/openthinclient/otc-manager-home/nfs/root/var/cache/archives/ -name "*.deb" -exec rm {} \;

    # remove cache files
    # rm -rf /home/openthinclient/otc-manager-home/nfs/root/var/cache/archives/1/*
    # rm -rf /home/openthinclient/otc-manager-home/nfs/root/var/cache/archives/2/*
    # rm -rf /home/openthinclient/otc-manager-home/nfs/root/var/cache/archives/3/*

    # remove nfs db from manager home
    rm /home/openthinclient/otc-manager-home/nfs/nfs-paths.db*

    # remove homes
    rm -rf /home/openthinclient/otc-manager-home/nfs/home/*

    # remove old logfiles from manager home
    rm -rf /home/openthinclient/otc-manager-home/logs/*

    # Remove unique server id
    ${OTC_INSTALL_PATH}bin/managerctl rm-server-id --home ${OTC_INSTALL_HOME}
fi

# delete ldap backups
if [ -d "/var/backups/openthinclient/ " ]; then
    find /var/backups/openthinclient/ -print -name "*\.ldiff\.*" -type f -exec rm -rf {} \;
fi

# cleanup teamviewer config
if [ -f "/opt/teamviewer9/config/global.conf" ]; then
    echo "==> Cleaning up teamviewer global.conf"
    rm /opt/teamviewer9/config/global.conf
fi

if [ -f "/opt/teamviewer9/config/openthinclient/client.conf" ]; then
    echo "==> Cleaning up /opt/teamviewer9/config/openthinclient/client.conf"
    rm /opt/teamviewer9/config/openthinclient/client.conf
fi
# /opt/teamviewer9/tv_bin/teamviewerd -d

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

echo "==> remove udev network rules to cleanup old interfaces"
if [ -f "/etc/udev/rules.d/70-persistent-net.rules" ]; then
    rm /etc/udev/rules.d/70-persistent-net.rules
fi

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

clean_logs() {
    echo $1
    echo $2
    for i in `find ${1} -name ${2} -type f`
    do
        >$i
    	ls -la $i
    	#rm $i
    done
}


clean_logs "/var/log/" "*\.log\.*"
clean_logs "/var/log/" "*\.0"
clean_logs "/var/log/" "*\.[0-9]*\.gz"

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

