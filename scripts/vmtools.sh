#!/bin/sh -eux
# Filename:     vmtools.sh
# Purpose:      install specific vm tools dependent on packer build type
#------------------------------------------------------------------------------

# set a default HOME_DIR environment variable if not set
HOME_DIR="${HOME_DIR:-/home/openthinclient}";

#env | sort
#set +u

function install_open_vm_tools {
    echo "==> Installing Open VM Tools"
    # Install open-vm-tools. Due to --no-intall-recommends require all packages
    apt-get install -y open-vm-tools open-vm-tools-dev open-vm-tools-desktop
    # Add /mnt/hgfs if you want shared folders with Vagrant
    # mkdir /mnt/hgfs
    rm -f $HOME_DIR/*.iso;
}

function install_vmware_tools {
    echo "==> Installing VMware Tools"
    mkdir -p /tmp/vmfusion;
    mkdir -p /tmp/vmfusion-archive;
    mount -o loop $HOME_DIR/linux.iso /tmp/vmfusion;
    tar xzf /tmp/vmfusion/VMwareTools-*.tar.gz -C /tmp/vmfusion-archive;
    #/tmp/vmfusion-archive/vmware-tools-distrib/vmware-install.pl --force-install;
	  /tmp/vmfusion-archive/vmware-tools-distrib/vmware-install.pl -d;
    umount /tmp/vmfusion;
    rm -rf  /tmp/vmfusion;
    rm -rf  /tmp/vmfusion-archive;
    rm -f $HOME_DIR/*.iso;
}

function install_virtualbox_tools {
    echo "=> Installing virtualbox tools"
	  apt-get install -y --no-install-recommends build-essential linux-headers-`uname -r` dkms
    mkdir -p /tmp/vbox;
    VBOX_VERSION="`cat /home/openthinclient/.vbox_version`";
    VBOX_ISO=$HOME_DIR/VBoxGuestAdditions_${VBOX_VERSION}.iso
    if [ ! -f $VBOX_ISO ] ; then
    wget -q http://download.virtualbox.org/virtualbox/${VBOX_VERSION}/VBoxGuestAdditions_${VBOX_VERSION}.iso \
        -O $VBOX_ISO
    fi
    mount -o loop $HOME_DIR/VBoxGuestAdditions_${VBOX_VERSION}.iso /tmp/vbox;
    sh /tmp/vbox/VBoxLinuxAdditions.run \
        || echo "VBoxLinuxAdditions.run exited $? and is suppressed." \
            "For more read https://www.virtualbox.org/ticket/12479";
    umount /tmp/vbox;
    rm -rf /tmp/vbox;
    rm -f $HOME_DIR/*.iso;
    apt-get remove -y build-essential
    
    echo "==> "echo "==> Adding user "openthinclient" to vboxsf group"
    sudo usermod -a -G vboxsf openthinclient    
}

echo "$PACKER_BUILDER_TYPE"

case "$PACKER_BUILDER_TYPE" in

virtualbox-iso|virtualbox-ovf)
    install_virtualbox_tools
    install_open_vm_tools
    ;;

vmware-iso|vmware-vmx)
    install_open_vm_tools
    ;;

parallels-iso|parallels-pvm)
    mkdir -p /tmp/parallels;
    mount -o loop $HOME_DIR/prl-tools-lin.iso /tmp/parallels;
    /tmp/parallels/install --install-unattended-with-deps \
      || (code="$?"; \
          echo "Parallels tools installation exited $code, attempting" \
          "to output /var/log/parallels-tools-install.log"; \
          cat /var/log/parallels-tools-install.log; \
          exit $code);
    umount /tmp/parallels;
    rm -rf /tmp/parallels;
    rm -f $HOME_DIR/*.iso;
    ;;

qemu)
    echo "Don't need anything for this one"
    ;;

*)
    echo "Unknown Packer Builder Type >> $PACKER_BUILDER_TYPE << selected.";
    echo "Known are virtualbox-iso|virtualbox-ovf|vmware-iso|vmware-vmx|parallels-iso|parallels-pvm.";
    ;;

esac
