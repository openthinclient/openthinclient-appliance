#!/bin/bash
# Filename:     openthinclient-gui.sh
# Purpose:      install openthinclient custom GUI and related packages
#------------------------------------------------------------------------------
export DEBIAN_FRONTEND="noninteractive"

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
chown root:root /etc/lightdm/lightdm.conf

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

echo "==> Deploying appliance wizard [0/4]:"
echo "==> Appliance wizard: Download nodejs [1/4]"
wget -q -O ${OTC_CUSTOM_DEPLOY_PATH}/appliance-wizard/nodejs.tar.xz "${NODEJS_URL}"

echo "==> Appliance wizard: Unpack nodejs [2/4]"
tar -xf ${OTC_CUSTOM_DEPLOY_PATH}/appliance-wizard/nodejs.tar.xz -C ${OTC_CUSTOM_DEPLOY_PATH}/appliance-wizard
NODE_DIR=$(tar -tf ${OTC_CUSTOM_DEPLOY_PATH}/appliance-wizard/nodejs.tar.xz | head -n 1)
PATH=$PATH:${OTC_CUSTOM_DEPLOY_PATH}/appliance-wizard/${NODE_DIR}bin

echo "==> Appliance wizard: Build frontend [3/4]"
cd ${OTC_CUSTOM_DEPLOY_PATH}/appliance-wizard/frontend/page || exit
npm config set update-notifier false
npm install
npm run build

echo "==> Appliance wizard: Deploy wizard [4/4]"
mkdir -p /usr/local/share/appliance-wizard
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/appliance-wizard/backend /usr/local/share/appliance-wizard
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/etc/systemd/system/configure-first-start-autologin.service /etc/systemd/system/configure-first-start-autologin.service
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/bin/configure-first-start-autologin.py /usr/local/bin/configure-first-start-autologin.py
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/etc/lightdm/lightdm-firststart-override.conf /etc/lightdm/lightdm-firststart-override.conf
mv /usr/local/share/appliance-wizard/backend/wizard-server.service /etc/systemd/system/wizard-server.service
mv /usr/local/share/appliance-wizard/backend/wizard-server.path /etc/systemd/system/wizard-server.path
mkdir -p /usr/local/share/appliance-wizard/frontend
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/appliance-wizard/frontend/browser /usr/local/share/appliance-wizard/frontend
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/appliance-wizard/frontend/browser/wizard-start.desktop /etc/xdg/autostart/wizard-start.desktop
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/appliance-wizard/frontend/page/dist /usr/local/share/appliance-wizard/backend
mv /usr/local/share/appliance-wizard/backend/dist /usr/local/share/appliance-wizard/backend/assets
mkdir -p /var/appliance-wizard
touch /var/appliance-wizard/RUN.FLAG
dos2unix /usr/local/share/appliance-wizard/backend/start.sh
chmod +x /usr/local/share/appliance-wizard/backend/start.sh
dos2unix /usr/local/share/appliance-wizard/frontend/browser/start.sh
chmod +x /usr/local/share/appliance-wizard/frontend/browser/start.sh

chown root:root /usr/local/share/appliance-wizard -R
chown root:root /etc/systemd/system/wizard-server.service
chown root:root /etc/systemd/system/wizard-server.path
chown root:root /etc/xdg/autostart/wizard-start.desktop

chmod +x /usr/local/bin/configure-first-start-autologin.py

systemctl enable wizard-server.service
systemctl enable wizard-server.path
systemctl enable configure-first-start-autologin.service

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

echo "==> Reading desktop configuration"
sudo -u openthinclient dbus-launch dconf dump /

echo "==> Setting preconfigured desktop configuration"
DCONF_CONFIG="${OTC_CUSTOM_DEPLOY_PATH}/dconf-backup.txt"

echo "==> Loading preconfigured desktop configuration"
sudo -u openthinclient dbus-launch dconf load / < ${DCONF_CONFIG}

echo "==> Setting openthinclient appliance desktop background"
sudo -u openthinclient dbus-launch gsettings writable org.mate.background picture-filename
sudo -u openthinclient dbus-launch gsettings set org.mate.background picture-filename '/usr/local/share/openthinclient/backgrounds/default.png'

echo "==> Disable key shortcut <Ctrl><Alt><Delete> in Mate-desktop environment"
sudo -u openthinclient dbus-launch dconf write /org/mate/settings-daemon/plugins/media-keys/power "''"

echo "==> Installing chromium web browser with --no-install-recommends"
apt-get install -y --no-install-recommends chromium

echo "==> Installing chromium web browser language packs with --no-install-recommends"
apt-get install -y --no-install-recommends chromium-l10n

echo "==> Creating chromium web browser managed policies directory"
mkdir -p /etc/chromium/policies/managed/

echo "==> Deploying chromium web browser managed policy"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/etc/chromium/policies/managed/*.json /etc/chromium/policies/managed/
chown root:root /etc/chromium/policies/managed/ -R

echo "==> Deploying chromium web browser master preferences file"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/etc/chromium/master_preferences /etc/chromium/
chown root:root /etc/chromium/ -R

# Validity: [from: Aug 17 00:00:00 UTC 2022 to: 15 Aug 23:59:59 2025]
echo "==> Deploying openthinclient-Livesupport trusted certificate"
mkdir -p /home/openthinclient/.config/icedtea-web/security/
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/live-support-cert/trusted.certs /home/openthinclient/.config/icedtea-web/security/
chmod 600 /home/openthinclient/.config/icedtea-web/security/trusted.certs

echo "==> Installing tigervnc-viewer with --no-install-recommends"
apt-get install -y --no-install-recommends tigervnc-viewer

echo "==> Installing pluma texteditor with --no-install-recommends"
apt-get install -y --no-install-recommends pluma

# FIX config dir - Temp workaround
OTC_HOME_CONFIG_DIR=/home/openthinclient/.config/

if [ -d $OTC_HOME_CONFIG_DIR ]; then
    echo "==> Setting ownership for $OTC_HOME_CONFIG_DIR to user \"openthinclient\""
    chown openthinclient:openthinclient ${OTC_HOME_CONFIG_DIR} -R
else
    echo "==> $OTC_HOME_CONFIG_DIR will be created"
    mkdir $OTC_HOME_CONFIG_DIR
    chown openthinclient:openthinclient ${OTC_HOME_CONFIG_DIR} -R
fi

exit 0