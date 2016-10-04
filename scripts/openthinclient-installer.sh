#!/usr/bin/env bash
# Filename:     openthinclient-installer.sh
# Purpose:      install new version of the openthinclient software package
#------------------------------------------------------------------------------

OTC_INSTALLER_NAME=otc-manager_unix_2_0_0.sh
OTC_INSTALLER_FULLPATH=/tmp/installer/${OTC_INSTALLER_NAME}

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

	    echo "==> Running managerctl install with predefined variables"
	    $OPENTHINCLIENT_INSTALL_PATH/bin/managerctl prepare-home --admin-password 0pen%TC --home $OTC_INSTALL_HOME > /dev/null 2>&1

        echo "==> Checking service status before start"
        $OPENTHINCLIENT_INSTALL_PATH/bin/service status
        echo "==> Starting the OTC manager service"
        $OPENTHINCLIENT_INSTALL_PATH/bin/service start
        echo "==> Checking service status after start"
        $OPENTHINCLIENT_INSTALL_PATH/bin/service status

        # symlink the service
        #ln -s OPENTHINCLIENT_INSTALL_PATH/bin/service /etc/init.d/openthinclient

    else
	    echo "==> $OPENTHINCLIENT_INSTALL_PATH doesn't exist. Installation was not successful"
    fi

else
	echo "==> $OTC_INSTALLER_FULLPATH doesn't exist. Installation can't be executed"
fi

exit 0
