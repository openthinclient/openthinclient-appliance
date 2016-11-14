#!/usr/bin/env bash
# Filename:     openthinclient-installer.sh
# Purpose:      install new version of the openthinclient software package
#------------------------------------------------------------------------------

OTC_INSTALLER_NAME=otc-manager_unix.sh
OTC_INSTALLER_FULLPATH=/tmp/installers/${OTC_INSTALLER_NAME}

OTC_INSTALLER_VARFILE=/tmp/data/installer/unattended-linux.varfile.txt

# Please sync these with the unattended linux-varfile
OPENTHINCLIENT_INSTALL_PATH=/opt/openthinclient/
# location of the home working directory
OTC_INSTALL_HOME=/home/openthinclient/otc-manager-home/


echo "==> Installing new openthinclient manager"
if [ -f $OTC_INSTALLER_FULLPATH ]; then
	echo "==> $OTC_INSTALLER_FULLPATH exists. Continue with installation"
	echo $OTC_INSTALLER_FULLPATH

	echo "==> Setting chmod +x for the installer binary: $OTC_INSTALLER_FULLPATH"
	chmod +x $OTC_INSTALLER_FULLPATH

	echo "==> Starting unattended installation with preconfigured varfile: $OTC_INSTALLER_VARFILE"
	echo $OTC_INSTALLER_FULLPATH -q -varfile $OTC_INSTALLER_VARFILE
	$OTC_INSTALLER_FULLPATH -q -varfile $OTC_INSTALLER_VARFILE

    echo "==> Checking for existing manager installation to prepare-home"
	if [ -f $OPENTHINCLIENT_INSTALL_PATH/bin/managerctl ]; then
	    echo "==> Running managerctl to check available distributions"
	    $OPENTHINCLIENT_INSTALL_PATH/bin/managerctl ls-distributions -v
	    echo $OPENTHINCLIENT_INSTALL_PATH/bin/managerctl ls-distributions -v

        echo "==> Checking mySQL database server status"
        mysqlrun=$(sudo service mysql status)
        if [ $? -ne 0 ]; then
            echo "==> Running managerctl install with predefined variables and default included H2 database"
	        $OPENTHINCLIENT_INSTALL_PATH/bin/managerctl prepare-home \
	        --admin-password 0pen%TC \
	        --home $OTC_INSTALL_HOME \
	        --db MYSQL \
	        --db-host localhost \
	        --db-name openthinclient \
	        --db-user openthinclient \
	        --db-password openthinclient > /dev/null 2>&1
        fi
             echo "==> Running managerctl install with predefined variables and mySQL database backend"
            $OPENTHINCLIENT_INSTALL_PATH/bin/managerctl prepare-home --admin-password 0pen%TC --home $OTC_INSTALL_HOME > /dev/null 2>&1

        echo "==> Starting the OTC manager service"
        $OPENTHINCLIENT_INSTALL_PATH/bin/openthinclient-manager start
        sleep 5
        echo "==> Checking service status after start"
        $OPENTHINCLIENT_INSTALL_PATH/bin/openthinclient-manager status

        # symlink the service
        #ln -s OPENTHINCLIENT_INSTALL_PATH/bin/openthinclient-manager /etc/init.d/openthinclient

    else
	    echo "==> $OPENTHINCLIENT_INSTALL_PATH doesn't exist. Installation was not successful"
    fi

else
	echo "==> $OTC_INSTALLER_FULLPATH doesn't exist. Installation can't be executed"
fi

exit 0
