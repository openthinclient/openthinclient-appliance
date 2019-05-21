#!/usr/bin/env bash
# Filename:     jre-oracle-8.sh installer.sh
# Purpose:      install oracle java jre version 8
#------------------------------------------------------------------------------

SYSARCH=`uname -m`
if [ $SYSARCH == x86_64 ]; then
wget -c http://develop.openthinclient.com/java/jdk-8u202-linux-x64.tar.gz -O /tmp/java_linux.tar.gz
else
wget -c http://develop.openthinclient.com/java/jdk-8u202-linux-i586.tar.gz -O /tmp/java_linux.tar.gz
fi

mkdir /opt/jdk
tar -zxf /tmp/java_linux.tar.gz -C /opt/jdk

update-alternatives --install /usr/bin/java java /opt/jdk/jdk1.8.0_202/bin/java 100
update-alternatives --install /usr/bin/javac javac /opt/jdk/jdk1.8.0_202/bin/javac 100


exit 0
