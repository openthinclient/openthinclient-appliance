#! /bin/bash

deviceToClean=$(mount | grep -w '/'  | awk '{print $1}')


echo -e "\n\n\n\n"
echo "######################################################################"
echo 
echo "The system will now fill up unused blocks on harddisk with 0 (ZEROS)"
echo "Keep in mind to shrink your virtual HD."
echo -e "E.g. \t \"VBoxManage modifyhd --compact my_hd.vdi\""
echo "Export your VM after shrinking. Please wait..."

zerofree $deviceToClean

echo -e "\n\n"
echo -e "\tHit Enter key to shut down the system."
read foo
poweroff -f



