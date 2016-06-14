#!/usr/bin/env bash
# Filename:     jre-oracle-8.sh installer.sh
# Purpose:      install oracle java jre version 8
#------------------------------------------------------------------------------

INSTALL="apt-get install -y --force-yes --no-install-recommends"
UPDATE="apt-get update"
PACKAGES="oracle-java8-installer oracle-java8-set-default"

echo "deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main"> /etc/apt/sources.list.d/webupd8team-java.list
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys EEA14886

echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections

eval "$UPDATE"
eval "$INSTALL $PACKAGES"


exit 0
