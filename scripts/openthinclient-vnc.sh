#!/usr/bin/env bash
# Filename:     openthinclient-vnc.sh
# Purpose:      install openthinclient custom VNC server and related packages
#------------------------------------------------------------------------------
export DEBIAN_FRONTEND="noninteractive"

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

SYSARCH=`uname -m`
if [ $SYSARCH == x86_64 ]; then
  cp -a ${OTC_CUSTOM_DEPLOY_PATH}/vnc/x11vnc_64 /usr/bin/x11vnc
  echo "==> Copying custom x11vnc 64bit binary script to /usr/bin"
else
  cp -a ${OTC_CUSTOM_DEPLOY_PATH}/vnc/x11vnc_32 /usr/bin/x11vnc
  echo "==> Copying custom x11vnc 32bit binary script to /usr/bin"
fi

echo "==> Setting executable bit and correct permissions for custom x11vnc in /usr/bin"
chmod +x /usr/bin/x11vnc
chown root:staff /usr/bin/x11vnc

echo "==> Installing python-pip and python-wheel for python package handling"
apt-get install -y python-pip python-wheel --no-install-recommends

echo "==> Copying websockify-0.8.0.tar.gz wheel to /usr/bin"
pip install ${OTC_CUSTOM_DEPLOY_PATH}/websockify-0.8.0.tar.gz

echo "==> Configure websockify service"
cat > /etc/systemd/system/websockify.service << EOF
[Unit]
Description=Start websockify at startup.
After=multi-user.target

[Service]
User=openthinclient
Group=openthinclient
Type=simple
ExecStart=/usr/local/bin/websockify 5900 --token-plugin OTCTokenPlugin
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable websockify.service
sudo systemctl daemon-reload

echo "==> Configure xvfb service"
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
After=multi-user.target xvfb.service

[Service]
User=openthinclient
Group=openthinclient
Type=simple
ExecStartPre=/bin/sleep 1
ExecStart=/usr/bin/x11vnc -display :2 -env FD_GEOM="1100x780x16" -forever -shared -rfbport 5910 -localhost
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable x11vnc.service
sudo systemctl daemon-reload

exit 0