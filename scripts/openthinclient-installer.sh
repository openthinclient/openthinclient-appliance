#!/usr/bin/env bash
# Filename:     openthinclient-installer.sh
# Purpose:      install new version of the openthinclient software package
#------------------------------------------------------------------------------

OPENTHINCLIENT_INSTALLER=otc-manager_unix_2_0_0.sh
OPENTHINCLIENT_FULLPATH=/tmp/data/installer/${OPENTHINCLIENT_INSTALLER}

if [ -f $OPENTHINCLIENT_FULLPATH ]; then
	echo "==> $OPENTHINCLIENT_FULLPATH exists. Continue with installation"
	echo $OPENTHINCLIENT_FULLPATH
	# move the installer to /opt
	mv $OPENTHINCLIENT_FULLPATH /opt
	# make it executable
	chmod +x /opt/OPENTHINCLIENT_INSTALLER
fi


exit 0
