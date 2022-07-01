#!/usr/bin/env bash -eux
# Filename:     print-server.sh
# Purpose:      install print server for openthinclient usage
#------------------------------------------------------------------------------
# set custom deploy path
OTC_CUSTOM_DEPLOY_PATH=/tmp/data/otc-custom-deploy

echo "==> Installing cups packages"
sudo apt-get -y install cups cups-client cups-bsd

echo "==> Installing cups driver packages"
sudo apt-get -y install printer-driver-gutenprint printer-driver-hpijs

echo "==> Installing cups pdf printer driver package"
sudo apt-get -y install printer-driver-cups-pdf

echo "==> Stopping cups service before config changes are applied"
sudo service cups stop
sleep 2

echo "==> Check that cups is stopped before config changes are made"
sudo service cups status

echo "==> Copying custom cups configuration file"
cp -a ${OTC_CUSTOM_DEPLOY_PATH}/etc/cups/cupsd.conf /etc/cups/cupsd.conf

echo "==> Setting correct permissions for custom cupsd.conf configuration"
chown root:lp /etc/cups/cupsd.conf

echo "==> Adding user "openthinclient" to lpadmin group"
sudo usermod -a -G lpadmin openthinclient

