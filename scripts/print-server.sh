#!/bin/bash 
# Filename:     print-server.sh
# Purpose:      install print server for openthinclient usage
#------------------------------------------------------------------------------
export DEBIAN_FRONTEND="noninteractive"
# set custom deploy path
OTC_CUSTOM_DEPLOY_PATH=/tmp/data/otc-custom-deploy

echo "==> Installing cups packages"
apt-get -y install cups cups-client cups-bsd

echo "==> Installing cups driver packages"
apt-get -y install printer-driver-gutenprint printer-driver-hpijs

echo "==> Installing cups pdf printer driver package"
apt-get -y install printer-driver-cups-pdf

echo "==> Stopping cups service before config changes are applied"
systemctl stop cups
sleep 2

echo "==> Copying custom cups configuration file"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/etc/cups/cupsd.conf /etc/cups/cupsd.conf

echo "==> Setting correct permissions for custom cupsd.conf configuration"
chown root:lp /etc/cups/cupsd.conf

echo "==> Adding user openthinclient to lpadmin group"
usermod -a -G lpadmin openthinclient