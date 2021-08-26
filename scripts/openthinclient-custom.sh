#!/usr/bin/env bash
# Filename:     openthinclient-custom.sh
# Purpose:      install openthinclient custom scripts and needed packages
#------------------------------------------------------------------------------

# set custom deploy path
OTC_CUSTOM_DEPLOY_PATH=/tmp/data/otc-custom-deploy

OTC_INSTALL_PATH=/opt/otc-manager/


echo "==> Deploying custom sudoers file for openthinclient user"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/etc/sudoers.d/90-openthinclient-appliance /etc/sudoers.d/90-openthinclient-appliance
chown root:root /etc/sudoers.d/90-openthinclient-appliance
chmod 0440 /etc/sudoers.d/90-openthinclient-appliance

echo "==> Deploying custom otc vimrc "
cp -a  ${OTC_CUSTOM_DEPLOY_PATH}/etc/vim/vimrc /etc/vim/vimrc

echo "==> Setting custom bashrc aliases for user"
USER_ALIASES_FILE=/home/openthinclient/.bash_aliases
ROOT_ALIASES_FILE=/root/.bash_aliases
ROOT_BASHRC_FILE=/root/.bashrc

read -r -d '' ALIASES << EOF
alias ll='ls -alF'
#alias la='ls -A'
#alias l='ls -CF'
EOF

echo "${ALIASES}"

echo "==> Setting custom bashrc aliases for user"
echo "${ALIASES}" > ${USER_ALIASES_FILE}

echo "==> Setting correct permission for ${USER_ALIASES_FILE}"
chown openthinclient:openthinclient ${USER_ALIASES_FILE}

echo "==> Setting custom bashrc aliases for root"
echo "${ALIASES}" > ${ROOT_ALIASES_FILE}

read -r -d '' ALIASINCLUDE << EOF

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi
EOF

echo "==> Including aliases in bashrc for root"
echo "${ALIASINCLUDE}" > ${ROOT_BASHRC_FILE}

echo "==> Creating custom .bash_profile and referencing .bashrc"
cat <<EOF >> /home/openthinclient/.bash_profile
if [ -f ~/.bashrc ]; then
source ~/.bashrc
fi
EOF
chown openthinclient:openthinclient /home/openthinclient/.bash_profile


echo "==> Adding sbin paths for openthinclient user"
echo 'export PATH="$PATH:/sbin:/usr/sbin:/usr/local/sbin"' > /home/openthinclient/.profile
echo 'if [ -r ~/.profile ]; then . ~/.profile; fi' > /home/openthinclient/.xsessionrc

echo "==> turn off screen blanking inside openthinclient VM"
cat <<EOF >> /home/openthinclient/.xsessionrc
# Turn off screen blanking
xset s off && xset -dpms

EOF
chown openthinclient:openthinclient /home/openthinclient/.xsessionrc

echo "==> Creating openthinclient directory in /usr/local/share"
OTCLOCALSHARE="/usr/local/share/openthinclient/"

if ! [ -d $OTCLOCALSHARE ]; then
	echo "==> $OTCLOCALSHARE will be created"
	mkdir $OTCLOCALSHARE
fi

echo "==> Copying custom bin scripts to /usr/local/bin"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/bin/openthinclient-manager /usr/local/bin/openthinclient-manager
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/bin/openthinclient-vmversion /usr/local/bin/openthinclient-vmversion

echo "==> Setting executable bit for custom bin scripts in /usr/local/bin"
chmod +x /usr/local/bin/openthinclient*
dos2unix /usr/local/bin/openthinclient*

echo "==> Copying custom tcos-ascii script to /usr/local/bin"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/bin/tcos-ascii /usr/local/bin/tcos-ascii
dos2unix /usr/local/bin/tcos-ascii
chmod +x /usr/local/bin/tcos-ascii

echo "==> Copying custom sbin scripts to /usr/local/sbin"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/sbin/openthinclient* /usr/local/sbin/
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/sbin/zerofree.sh /usr/local/sbin/

echo "==> Setting executable bit for custom sbin scripts in /usr/local/sbin"
chmod +x /usr/local/sbin/openthinclient*
dos2unix /usr/local/sbin/openthinclient*
chmod +x /usr/local/sbin/zerofree.sh
dos2unix /usr/local/sbin/zerofree.sh

echo "==> Deploying openthinclient ldap cronjob file"
cp -a  ${OTC_CUSTOM_DEPLOY_PATH}/etc/cron.d/openthinclient_ldap_backup /etc/cron.d/openthinclient_ldap_backup
chown root:root /etc/cron.d/openthinclient_ldap_backup
chmod +x /etc/cron.d/openthinclient_ldap_backup
dos2unix /etc/cron.d/openthinclient_ldap_backup

echo "==> Deploying openthinclient-documentation directory"
if [ -d ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/share/openthinclient/documentation/ ]; then
    cp -a ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/share/openthinclient/documentation/ /usr/local/share/openthinclient/documentation/
else
    echo "==> Deploying openthinclient-documentation directory failed"
fi


echo "==> Creating openthinclient vm version information"
VERSION_FILE="/usr/local/share/openthinclient/openthinclient-vm-version"
touch $VERSION_FILE

echo "==> Populating openthinclient vm version information"
if [ -f ${VERSION_FILE} ]; then
    echo "==> Populating already existing openthinclient vm version ${VERSION_FILE}"
    echo "===================" >>  ${VERSION_FILE}
    PLATFORM_MSG=$(printf 'openthinclient %s' "$OTC_APPLIANCE_VERSION")
    BUILT_MSG=$(printf 'built %s' $(date +%Y-%m-%d))
    printf '%s%-30s%10s\n' " " "${PLATFORM_MSG}" "${BUILT_MSG}" >> ${VERSION_FILE}
    echo "===================" >>  ${VERSION_FILE}
    echo "Operating system:" >>  ${VERSION_FILE}
    lsb_release -d -s >>  ${VERSION_FILE}
    echo "===================" >>  ${VERSION_FILE}
    #${OTC_INSTALL_PATH}bin/managerctl ls-distributions -v >>  ${VERSION_FILE}
else
    echo "==> Populating openthinclient VM information failed. File not found"
fi

echo "==> Deploying openthinclient grub background image"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/grub_background/desktopB_1920x1200.png /boot/grub/desktopB_1920x1200.png
echo 'GRUB_BACKGROUND="/boot/grub/desktopB_1920x1200.png"' >> /etc/default/grub 


if [ $PACKER_BUILDER_TYPE == 'hyperv-iso' ]; then
  echo "Installing custom kernel grub configuration for Hyper-V"
  sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="quiet"/GRUB_CMDLINE_LINUX_DEFAULT="quiet video=hyperv_fb:1600x900"/g' /etc/default/grub
else
  echo "Using default kernel grub configuration for virtualbox/VMware builds"
fi

echo "==> Deploying openthinclient grub color configuration"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/etc/grub.d/05_debian_theme /etc/grub.d/05_debian_theme
chown root:root /etc/grub.d/05_debian_theme
chmod 755 /etc/grub.d/05_debian_theme

cp -a ${OTC_CUSTOM_DEPLOY_PATH}/etc/grub.d/40_otc-shrinker /etc/grub.d/40_otc-shrinker
chown root:root /etc/grub.d/40_otc-shrinker
chmod 755 /etc/grub.d/40_otc-shrinker

echo "==> Installing zerofree package for otc-shrinker script"
apt-get install -y zerofree

echo "==> Updating grub configuration"
update-grub

echo "==> setting nofile limits"
cat <<EOF >> /etc/security/limits.conf
*               -   nofile  	65535
openthinclient	-  	nofile  	65535
root            -  	nofile  	65535
EOF

exit 0
