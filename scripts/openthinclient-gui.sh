#!/usr/bin/env bash
# Filename:     openthinclient-gui.sh
# Purpose:      install openthinclient custom GUI and related packages
#------------------------------------------------------------------------------

INSTALL="apt-get install -y"
UPDATE="apt-get update"
PACKAGES="mate-desktop-environment-core"

eval "$UPDATE"
eval "$INSTALL $PACKAGES"


echo "==> Installing xserver-xorg"
apt-get install -y xserver-xorg

echo "==> Installing lightdm with --no-install-recommends"
apt-get install -y --no-install-recommends lightdm

# echo "==> Installing Teamviewer9 debian package if present"
# TEAMVIEWER_INSTALLER="teamviewer_linux.deb"
#
# if [ -f /tmp/data/${TEAMVIEWER_INSTALLER} ]; then
# 	echo "==> Installing already downloaded Teamviewer9 debian package"
# 	dpkg -i /tmp/data/${TEAMVIEWER_INSTALLER}
# else
#     echo "==> Downloading Teamviewer9 debian package from official source"
#     wget -c http://download.teamviewer.com/download/version_9x/teamviewer_linux.deb -P /tmp/data/
#     if [ -f /tmp/data/${TEAMVIEWER_INSTALLER} ]; then
# 	    echo "==> Installing Teamviewer debian package"
# 	    dpkg -i /tmp/data/${TEAMVIEWER_INSTALLER}
# 	 else
#         echo "==> No Teamviewer9 package provided or download failed. Nothing to be installed"
# 	 fi
# fi

# setting otc custom deploy variables
OTC_CUSTOM_DEPLOY_PATH=/tmp/data/otc-custom-deploy
OTCLOCALSHARE="/usr/local/share/openthinclient/"
if ! [ -d $OTCLOCALSHARE ]; then
	echo "==> $OTCLOCALSHARE will be created"
	mkdir $OTCLOCALSHARE
fi

echo "==> Creating $OTCLOCALSHARE backgrounds dir"
mkdir $OTCLOCALSHARE/backgrounds/

echo "==> Creating $OTCLOCALSHARE icons dir"
mkdir $OTCLOCALSHARE/icons/

echo "==> Copying custom GUI changes to $OTCLOCALSHARE"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/share/openthinclient/backgrounds/ $OTCLOCALSHARE/

cp -a ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/share/openthinclient/icons/ $OTCLOCALSHARE/


echo "==> Deploying custom lightdm greeter"
cp -a  ${OTC_CUSTOM_DEPLOY_PATH}/etc/lightdm/lightdm-gtk-greeter.conf /etc/lightdm/lightdm-gtk-greeter.conf
# Fix permissions

echo "==> Deploying custom lightdm.conf"
cp -a  ${OTC_CUSTOM_DEPLOY_PATH}/etc/lightdm/lightdm.conf /etc/lightdm/lightdm.conf

echo "==> Deploying lightdm-dmrc-fix"
cp -a  ${OTC_CUSTOM_DEPLOY_PATH}/etc/21-lightdm-locale-fix /etc/X11/Xsession.d/21-lightdm-locale-fix
chown root:root /etc/X11/Xsession.d/21-lightdm-locale-fix

echo "==> Deploying lightdm fix for default user setting"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/bin/openthinclient-default-user-fix /usr/local/bin/openthinclient-default-user-fix
chmod +x /usr/local/bin/openthinclient-default-user-fix

echo "==> Deploying desktop icons for openthinclient user desktop"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/desktop-icons/ /home/openthinclient/Desktop/

echo "==> Installing dconf-tools"
apt-get install -y dconf-tools

echo "==> Installing mate-applets and mate-themes"
apt-get install -y mate-applets mate-themes

echo "==> Installing mate-utils"
apt-get install -y mate-utils


echo "==> Installing gnome-system-tools"
apt-get install -y gnome-system-tools

echo "==> Installing mate-system-monitor"
apt-get install -y mate-system-monitor --no-install-recommends

echo "==> Installing evince PDF viewer"
apt-get install -y evince


# workaround
/etc/init.d/lightdm start

#xhost
#export DISPLAY=:0
#env
#env |grep DISPLAY

#xhost +
#export DISPLAY=:0.0

# get object-id-list
#DISPLAY=:0 dbus-launch gsettings get org.mate.panel object-id-list
#DISPLAY=:0 dbus-launch gsettings get org.mate.panel toplevel-id-list
#dbus-launch --exit-with-session gsettings get org.mate.panel object-id-list
#gsettings get org.mate.panel object-id-list
#gsettings list-recursively org.mate.panel

echo "==> Reading desktop configuration via dconf"
dbus-launch dconf dump /
echo "==> End Reading desktop configuration via dconf"

echo "==> Setting preconfigured desktop configuration via dconf"
DCONF_CONFIG="${OTC_CUSTOM_DEPLOY_PATH}/dconf-backup.txt"

echo "dbus-launch dconf load < / $DCONF_CONFIG"
dbus-launch dconf load / < ${DCONF_CONFIG}


echo "==> Setting openthinclient Pales desktop background"
dbus-launch gsettings writable org.mate.background picture-filename
dbus-launch gsettings set org.mate.background picture-filename '/usr/local/share/openthinclient/backgrounds/openthinclient-server-Desktop-Pales.jpg'


#echo "==> Adding openthinclient manager icon to top panel"
#dbus-launch --exit-with-session gsettings set org.mate.panel.object:/org/mate/panel/objects/otc-manager/ object-type '"launcher"'
#dbus-launch --exit-with-session gsettings set org.mate.panel.object:/org/mate/panel/objects/otc-manager/ toplevel-id 'top'
#dbus-launch --exit-with-session gsettings set org.mate.panel.object:/org/mate/panel/objects/otc-manager/ launcher-location '"/home/openthinclient/Desktop/openthinclient Legacy WebStart Manager.desktop"'
#dbus-launch --exit-with-session gsettings set org.mate.panel.object:/org/mate/panel/objects/otc-manager/ position '20'
#dbus-launch --exit-with-session gsettings set org.mate.panel.object:/org/mate/panel/objects/otc-manager/ panel-right-stick 'false'
##dbus-launch --exit-with-session gsettings set org.mate.panel object-id-list "`gsettings get org.mate.panel object-id-list | sed 's/]$//g'`, 'otc-manager' ]"
#dbus-launch --exit-with-session gsettings set org.mate.panel object-id-list "`dbus-launch --exit-with-session gsettings get org.mate.panel object-id-list | sed 's/]$//g'`, 'otc-manager' ]"
#
#echo "==> Adding openthinclient restart icon to top panel"
#dbus-launch --exit-with-session gsettings set org.mate.panel.object:/org/mate/panel/objects/otc-restart/ toplevel-id 'top'
#dbus-launch --exit-with-session gsettings set org.mate.panel.object:/org/mate/panel/objects/otc-restart/ launcher-location '"/home/openthinclient/Desktop/openthinclient service restart.desktop"'
#dbus-launch --exit-with-session gsettings set org.mate.panel.object:/org/mate/panel/objects/otc-restart/ position '30'
#dbus-launch --exit-with-session gsettings set org.mate.panel.object:/org/mate/panel/objects/otc-restart/ panel-right-stick 'false'
#dbus-launch --exit-with-session gsettings set org.mate.panel.object:/org/mate/panel/objects/otc-restart/ object-type '"launcher"'
#dbus-launch --exit-with-session gsettings set org.mate.panel object-id-list "`dbus-launch --exit-with-session gsettings get org.mate.panel object-id-list | sed 's/]$//g'`, 'otc-restart' ]"
#
#
#echo "==> Adding firefox icon to top panel"
#dbus-launch --exit-with-session gsettings set org.mate.panel.object:/org/mate/panel/objects/firefox/ toplevel-id 'top'
#dbus-launch --exit-with-session gsettings set org.mate.panel.object:/org/mate/panel/objects/firefox/ launcher-location '"/usr/share/applications/firefox-esr.desktop"'
#dbus-launch --exit-with-session gsettings set org.mate.panel.object:/org/mate/panel/objects/firefox/ position '40'
#dbus-launch --exit-with-session gsettings set org.mate.panel.object:/org/mate/panel/objects/firefox/ panel-right-stick 'false'
#dbus-launch --exit-with-session gsettings set org.mate.panel.object:/org/mate/panel/objects/firefox/ object-type '"launcher"'
#dbus-launch --exit-with-session gsettings set org.mate.panel object-id-list "`dbus-launch --exit-with-session gsettings get org.mate.panel object-id-list | sed 's/]$//g'`, 'firefox' ]"


# FIX config dir - Temp workaround
OTC_HOME_CONFIG_DIR=/home/openthinclient/.config/

if ! [ -d $OTC_HOME_CONFIG_DIR ]; then
	echo "==> $OTC_HOME_CONFIG_DIR will be created"
	mkdir $OTC_HOME_CONFIG_DIR
	# chown openthinclient:openthinclient ${OTC_HOME_CONFIG_DIR} -R
fi
chown openthinclient:openthinclient ${OTC_HOME_CONFIG_DIR} -R

echo "==> Installing firefox web browser with --no-install-recommends"
apt-get install -y --no-install-recommends firefox-esr

echo "==> Installing firefox web browser german language file with --no-install-recommends"
apt-get install -y --no-install-recommends firefox-esr-l10n-de


if [ -d ${OTC_CUSTOM_DEPLOY_PATH}/mozilla/ ]; then
    echo "==> Deploying custom openthinclient mozilla settings"
	chown openthinclient:openthinclient ${OTC_HOME_CONFIG_DIR} -R
	cp -a ${OTC_CUSTOM_DEPLOY_PATH}/mozilla/ /home/openthinclient/
    mv /home/openthinclient/mozilla /home/openthinclient/.mozilla
    chown openthinclient:openthinclient /home/openthinclient/.mozilla/ -R
    chmod 700 /home/openthinclient/.mozilla/
    # Fix mozilla cache dir
    chown openthinclient:openthinclient /home/openthinclient/.cache/ -R
else
    echo "==> Deploying custom openthinclient mozilla settings failed"
fi


echo "==> Deploying .java default settings for the openthinclient manager"
tar xvfz ${OTC_CUSTOM_DEPLOY_PATH}/dotjava.tar.gz -C /home/openthinclient/
chown openthinclient:openthinclient /home/openthinclient/.java/ -R
chmod 700 /home/openthinclient/.java/

echo "==> Deploying Workaround to fix the german keyboard layout after session login: create autostart dir"
CONFIG_AUTOSTART_DIR=/home/openthinclient/.config/autostart/
[ ! -d $CONFIG_AUTOSTART_DIR ] && mkdir -p $CONFIG_AUTOSTART_DIR

echo "==> Deploying Workaround to fix the german keyboard layout after session login: create autostart icon"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/home/openthinclient/config/autostart/keyboard-layout-fix.desktop /home/openthinclient/.config/autostart/keyboard-layout-fix.desktop
chown openthinclient:openthinclient /home/openthinclient/.config/autostart/keyboard-layout-fix.desktop

echo "==> Deploying Workaround to fix the german keyboard layout after session login: bash script"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/bin/openthinclient-keyboard-layout-fix /usr/local/bin/openthinclient-keyboard-layout-fix
chmod +x /usr/local/bin/openthinclient-keyboard-layout-fix

echo "==> Installing xtightvncviewer with --no-install-recommends"
apt-get install -y --no-install-recommends xtightvncviewer

echo "==> Installing pluma texteditor with --no-install-recommends"
apt-get install -y --no-install-recommends pluma

exit 0
