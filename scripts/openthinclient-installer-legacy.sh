#!/usr/bin/env bash
# Filename:     openthinclient-installer-legacy.sh
# Purpose:      install legacy version of the openthinclient software package
#------------------------------------------------------------------------------

INSTALL="apt-get install -y --force-yes --no-install-recommends"
UPDATE="apt-get update"
PACKAGES="libxrender1 libxtst6"
OPENTHINCLIENT_INSTALLER=openthinclient-2.1-Pales.jar
OPENTHINCLIENT_FULLPATH=/tmp/data/installer-legacy/${OPENTHINCLIENT_INSTALLER}

eval "$INSTALL $PACKAGES"

if [ -f $OPENTHINCLIENT_FULLPATH ]; then
	echo "==> $OPENTHINCLIENT_FULLPATH exists. Continue with installation"
	echo $OPENTHINCLIENT_FULLPATH

	# provoke an exception to automate the installer
    echo -e '\n' | java -jar /tmp/data/installer-legacy/${OPENTHINCLIENT_INSTALLER} -console || /bin/true
    # move it to /opt
    pwd
    mv /usr/local/openthinclient /opt
    chmod -R g+w /opt/openthinclient

    echo "==> removing rpcbind package"
    apt-get remove rpcbind

    # check, whether it starts automatically
    ln -s /opt/openthinclient/bin/start.sh /etc/init.d/openthinclient
    update-rc.d openthinclient defaults
fi

# This doesn’t work properly. Also we now remove rpcbind completely
#update-rc.d -f rpcbind remove
#ln -snf /bin/true /etc/init.d/rpcbind || /bin/true

# deploy special sources.lst
#SOURCES_LIST="/opt/openthinclient/server/default/data/nfs/root/etc/sources.list"
#
#mkdir -p /var/www/openthinclient/manager-rolling
#sudo chown -R www-data:www-data /var/www/openthinclient/
#sudo chmod -R g+w /var/www/openthinclient
#ouch /var/www/openthinclient/manager-rolling/packages
#u -c "archive_metadata /var/www/openthinclient/manager-rolling" vagrant

#echo "==> restarting openthinclient service“
#/etc/init.d/openthinclient restart
exit 0
