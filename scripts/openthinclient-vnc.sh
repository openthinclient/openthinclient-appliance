#!/usr/bin/env bash
# Filename:     openthinclient-vnc.sh
# Purpose:      install openthinclient custom VNC server and related packages
#------------------------------------------------------------------------------

INSTALL="apt-get install -y"
UPDATE="apt-get update"
PACKAGES="openbox"

eval "$UPDATE"
eval "$INSTALL $PACKAGES"

FBOX_LASTWALLPAPER=/home/openthinclient/.fluxbox/lastwallpaper

# set custom deploy path
OTC_CUSTOM_DEPLOY_PATH=/tmp/data/otc-custom-deploy

echo "==> Installing xvfb with --no-install-recommends"
apt-get install -y --no-install-recommends xvfb

echo "==> Installing x11vnc with --no-install-recommends"
apt-get install -y --no-install-recommends x11vnc

# openbox configuration
echo "==> Creating openbox config dir"
OPENBOX_CONFIG_DIR=/home/openthinclient/.config/openbox/
[ ! -d $OPENBOX_CONFIG_DIR ] && mkdir -p $OPENBOX_CONFIG_DIR

echo "==> Deploying custom openbox configuration for openthinclient user"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/home/openthinclient/config/openbox/rc.xml /home/openthinclient/.config/openbox/rc.xml
chown openthinclient:openthinclient /home/openthinclient/.config/openbox/ -R

echo "==> Copying custom openthinclient-vnc-start script to /usr/local/bin"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/bin/openthinclient-vnc-starter /usr/local/bin/openthinclient-vnc-starter
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/usr/local/bin/openthinclient-vnc-xvfb /usr/local/bin/openthinclient-vnc-xvfb

echo "==> Setting executable bit for openthinclient-vnc-start scripts in /usr/local/bin"
chmod +x /usr/local/bin/openthinclient-vnc-starter
chmod +x /usr/local/bin/openthinclient-vnc-xvfb

echo "==> Copying custom 11vnc binary script to /usr/bin"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/x11vnc /usr/bin/x11vnc

echo "==> Setting executable bit and correct permissions for custom x11vnc in /usr/bin"
chmod +x /usr/bin/x11vnc
chown root:staff /usr/bin/x11vnc


echo "==> Configure x11vnc service"
cat > /etc/systemd/system/xvfb.service << EOF
[Unit]
Description=Start xvfb at startup.
After=multi-user.target

[Service]
User=openthinclient
Group=openthinclient
Environment=DISPLAY=:2
Type=simple
ExecStart=/usr/local/bin/openthinclient-vnc-xvfb
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable xvfb.service
sudo systemctl daemon-reload

echo "==> Configure x11vnc service"
cat > /etc/systemd/system/x11vnc.service << EOF
[Unit]
Description=Start x11vnc at startup.
After=multi-user.target

[Service]
User=openthinclient
Group=openthinclient
Environment="UNIXPW_DISABLE_LOCALHOST=1"
Environment="UNIXPW_DISABLE_SSL=1"
Type=simple
# ExecStart=/usr/bin/x11vnc -create -env FD_PROG=/usr/local/bin/openthinclient-vnc-starter -env X11VNC_FINDDISPLAY_ALWAYS_FAILS=1 -env FD_GEOM="1100x780x16" -env X11VNC_CREATE_GEOM="1100x780x16" -forever -shared -unixpw openthinclient
ExecStart=/usr/bin/x11vnc -display :2 -env FD_GEOM="1100x780x16" -forever -shared -unixpw
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable x11vnc.service
sudo systemctl daemon-reload

exit 0