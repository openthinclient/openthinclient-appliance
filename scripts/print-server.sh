#!/usr/bin/env bash -eux
# Filename:     print-server.sh
# Purpose:      install print server for openthinclient usage
#------------------------------------------------------------------------------

echo "==> Installing cups packages"
sudo apt-get -y install cups cups-client cups-bsd

echo "==> Installing cups driver packages"
sudo apt-get -y install printer-driver-gutenprint printer-driver-hpijs

echo "==> Installing cups pdf printer package"
sudo apt-get -y install cups-pdf

echo "==> Enabling cups local print sharing"
sudo cupsctl --share-printers

echo "==> Enabling cups remote administration"
sudo cupsctl --remote-admin
/etc/init.d/cups reload
