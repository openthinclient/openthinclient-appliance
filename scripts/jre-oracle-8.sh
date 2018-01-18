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

# Workaround because of latest oracle java update
apt-get install -y oracle-java8-installer || true \
&& cd /var/lib/dpkg/info \
&& sed -i 's|JAVA_VERSION=8u151|JAVA_VERSION=8u162|' oracle-java8-installer.* \
&& sed -i 's|PARTNER_URL=http://download.oracle.com/otn-pub/java/jdk/8u151-b12/e758a0de34e24606bca991d704f6dcbf/|PARTNER_URL=http://download.oracle.com/otn-pub/java/jdk/8u162-b12/0da788060d494f5095bf8624735fa2f1/|' oracle-java8-installer.* \
&& sed -i 's|SHA256SUM_TGZ="8062f34f69dd1f1991bff517df52da606c53f5fa0d6677ceb46df30e93b53a70"|SHA256SUM_TGZ="eecf88dbcf7c78d236251d44350126f1297a522f2eab974b4027ef20f7a6fb24"|' oracle-java8-installer.* \
&& sed -i 's|J_DIR=jdk1.8.0_151|J_DIR=jdk1.8.0_162|' oracle-java8-installer.* \

eval "$INSTALL $PACKAGES"

exit 0
