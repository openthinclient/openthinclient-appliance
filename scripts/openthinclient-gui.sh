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

echo "==> Installing network-manager and network-manager-gnome with --no-install-recommends"
apt-get install -y network-manager network-manager-gnome --no-install-recommends

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

echo "==> Deploying openthinclient LightDM/GTK-greeter configuration"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/etc/lightdm/lightdm.conf /etc/lightdm/lightdm.conf

echo -ne "==> LightDM-openthinclient-greeter [0/4] deploying\r"
mkdir -p /usr/local/share/lightdm/greeters/
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/share/lightdm/greeters/lightdm-openthinclient-greeter.desktop /usr/local/share/lightdm/greeters/
echo -ne "==> LightDM-openthinclient-greeter [1/4] deployed \r"
sleep 0.3

cp -a ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/bin/openthinclient-greeter.py /usr/local/bin/
chmod +x /usr/local/bin/openthinclient-greeter.py
echo -ne "==> LightDM-openthinclient-greeter [2/4] deployed \r"
sleep 0.3

mkdir -p /usr/local/share/openthinclient-greeter/
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/share/openthinclient-greeter/* /usr/local/share/openthinclient-greeter/
echo -ne "==> LightDM-openthinclient-greeter [3/4] deployed \r"
sleep 0.3

mkdir -p /var/lib/lightdm/.cache/openthinclient-greeter/
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/var/lib/lightdm/.cache/openthinclient-greeter/state /var/lib/lightdm/.cache/openthinclient-greeter/
chown -R lightdm:lightdm /var/lib/lightdm/.cache/openthinclient-greeter
echo -ne "==> LightDM-openthinclient-greeter [4/4] deployed \r"
echo -ne '\n'

echo "==> Disable reboot for ctrl-alt-delete keyboard combination"
rm /lib/systemd/system/ctrl-alt-del.target
ln -s /dev/null /lib/systemd/system/ctrl-alt-del.target
systemctl daemon-reload

echo "==> Deploying desktop icons for openthinclient user desktop"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/desktop-icons/ /home/openthinclient/Desktop/
chmod +x /home/openthinclient/Desktop/*.desktop

echo "==> Installing dconf packages"
apt-get install -y dconf-editor dconf-cli

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

echo "==> Installing arandr"
apt-get install -y arandr


# workaround
#/etc/init.d/lightdm start

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

echo "dbus-launch dconf load / < $DCONF_CONFIG"
dbus-launch dconf load / < ${DCONF_CONFIG}

echo "==> Setting openthinclient appliance desktop background"
dbus-launch gsettings writable org.mate.background picture-filename
dbus-launch gsettings set org.mate.background picture-filename '/usr/local/share/openthinclient/backgrounds/2019_1_magenta_2560x1440.jpg'

echo "==> disable unwanted <Ctrl><Alt><Delete> restart inside mate desktop environment"
dbus-launch dconf write /org/mate/settings-daemon/plugins/media-keys/power "''"

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

echo "==> Installing xtightvncviewer with --no-install-recommends"
apt-get install -y --no-install-recommends xtightvncviewer

echo "==> Installing pluma texteditor with --no-install-recommends"
apt-get install -y --no-install-recommends pluma

exit 0
