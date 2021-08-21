
variable "appliance_version" {
  type    = string
  default = "2021.2"
}

variable "cpus" {
  type    = string
  default = "2"
}

variable "disk_size" {
  type    = string
  default = "20480"
}

variable "headless" {
  type    = string
  default = "true"
}

variable "hostname" {
  type    = string
  default = "openthinclient-server"
}

variable "http_proxy" {
  type    = string
  default = "${env("http_proxy")}"
}

variable "https_proxy" {
  type    = string
  default = "${env("https_proxy")}"
}

variable "iso_checksum" {
  type    = string
  default = "c433254a7c5b5b9e6a05f9e1379a0bd6ab3323f89b56537b684b6d1bd1f8b6ad"
}

variable "iso_url" {
  type    = string
  default = "https://cdimage.debian.org/cdimage/archive/10.10.0/amd64/iso-cd/debian-10.10.0-amd64-netinst.iso"
}

variable "memory" {
  type    = string
  default = "3072"
}

variable "no_proxy" {
  type    = string
  default = "${env("no_proxy")}"
}

variable "otc_manager_database_pass" {
  type    = string
  default = "openthinclient"
}

variable "otc_manager_database_user" {
  type    = string
  default = "openthinclient"
}

variable "otc_manager_default_pass" {
  type    = string
  default = "0pen%TC"
}

variable "otc_manager_install_home" {
  type    = string
  default = "/home/openthinclient/otc-manager-home/"
}

variable "otc_manager_install_path" {
  type    = string
  default = "/opt/otc-manager/"
}

variable "ssh_name" {
  type    = string
  default = "openthinclient"
}

variable "ssh_pass" {
  type    = string
  default = "0pen%TC"
}

variable "virtualbox_guest_os_type" {
  type    = string
  default = "Debian_64"
}

variable "vm_description" {
  type    = string
  default = "openthinclient is a Free Open Source Thin Client Solution consisting of a Linux based operating system along with a comprehensive Java based management GUI and server component. It is intended for environments where a medium to large number of Thin Clients must be supported and managed efficiently. Offering flexibility unheard of in the world of proprietary Thin Client Solutions, openthinclient empowers developers and integrators to create advanced Thin Client solutions... for free. www.openthinclient.org"
}

variable "vm_name" {
  type    = string
  default = "openthinclient-Appliance-2021.2"
}

variable "vmware_guest_os_type" {
  type    = string
  default = "ubuntu-64"
}

variable "vmx_post_connectiontype" {
  type    = string
  default = "bridged"
}

source "hyperv-iso" "hyperv" {
  boot_command       = ["<esc><wait>", "install <wait>", "preseed/url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/preseed.cfg ", "debian-installer=en_US auto locale=en_US kbd-chooser/method=us ", "keyboard-configuration/xkb-keymap=us <wait>", "netcfg/get_hostname=${var.hostname} <wait>", "netcfg/get_domain=${var.hostname} <wait>", "fb=false debconf/frontend=noninteractive ", "keyboard-configuration/modelcode=SKIP keyboard-configuration/layout=USA ", "keyboard-configuration/variant=USA console-setup/ask_detect=false ", "<enter><wait>"]
  disk_size          = "${var.disk_size}"
  enable_secure_boot = false
  generation         = 1
  headless           = "${var.headless}"
  http_directory     = "debian10_64"
  http_port_max      = 9001
  http_port_min      = 9001
  iso_checksum       = "${var.iso_checksum}"
  iso_url            = "${var.iso_url}"
  memory             = "${var.memory}"
  output_directory   = "builds/output-${var.vm_name}-hyperv-iso"
  shutdown_command   = "echo ${var.ssh_pass} | sudo -S shutdown -P now"
  ssh_password       = "${var.ssh_pass}"
  ssh_timeout        = "60m"
  ssh_username       = "${var.ssh_name}"
  vm_name            = "${var.vm_name}"
}

source "virtualbox-iso" "vbox" {
  boot_command        = ["<esc><wait>", "install <wait>", "preseed/url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/preseed.cfg ", "debian-installer=en_US auto locale=en_US kbd-chooser/method=us ", "keyboard-configuration/xkb-keymap=us <wait>", "netcfg/get_hostname=${var.hostname} <wait>", "netcfg/get_domain=${var.hostname} <wait>", "fb=false debconf/frontend=noninteractive ", "keyboard-configuration/modelcode=SKIP keyboard-configuration/layout=USA ", "keyboard-configuration/variant=USA console-setup/ask_detect=false ", "<enter><wait>"]
  disk_size           = "${var.disk_size}"
  guest_os_type       = "${var.virtualbox_guest_os_type}"
  headless            = "${var.headless}"
  http_directory      = "debian10_64"
  http_port_max       = 9001
  http_port_min       = 9001
  iso_checksum        = "${var.iso_checksum}"
  iso_url             = "${var.iso_url}"
  output_directory    = "builds/output-${var.vm_name}-virtualbox-iso"
  post_shutdown_delay = "30s"
  shutdown_command    = "echo ${var.ssh_pass} | sudo -S shutdown -P now"
  ssh_password        = "${var.ssh_pass}"
  ssh_username        = "${var.ssh_name}"
  ssh_wait_timeout    = "60m"
  vboxmanage          = [["modifyvm", "{{ .Name }}", "--vram", "32"], ["modifyvm", "{{ .Name }}", "--cpus", "1"], ["modifyvm", "{{ .Name }}", "--memory", "${var.memory}"], ["modifyvm", "{{ .Name }}", "--description", "${var.vm_description}"]]
  vboxmanage_post     = [["modifyvm", "{{ .Name }}", "--vram", "32"], ["modifyvm", "{{ .Name }}", "--cpus", "1"], ["modifyvm", "{{ .Name }}", "--memory", "${var.memory}"]]
  vm_name             = "${var.vm_name}"
}

source "vmware-iso" "vmware" {
  boot_command     = ["<esc><wait>", "install <wait>", "preseed/url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/preseed.cfg ", "debian-installer=en_US auto locale=en_US kbd-chooser/method=us ", "keyboard-configuration/xkb-keymap=us <wait>", "netcfg/get_hostname=${var.hostname} <wait>", "netcfg/get_domain=${var.hostname} <wait>", "fb=false debconf/frontend=noninteractive ", "keyboard-configuration/modelcode=SKIP keyboard-configuration/layout=USA ", "keyboard-configuration/variant=USA console-setup/ask_detect=false ", "<enter><wait>"]
  disk_size        = "${var.disk_size}"
  guest_os_type    = "${var.vmware_guest_os_type}"
  headless         = "${var.headless}"
  http_directory   = "debian10_64"
  http_port_max    = 9001
  http_port_min    = 9001
  iso_checksum     = "${var.iso_checksum}"
  iso_url          = "${var.iso_url}"
  output_directory = "builds/output-${var.vm_name}-vmware-iso"
  shutdown_command = "echo ${var.ssh_pass} | sudo -S shutdown -P now"
  ssh_password     = "${var.ssh_pass}"
  ssh_username     = "${var.ssh_name}"
  ssh_wait_timeout = "60m"
  vm_name          = "${var.vm_name}"
  vmx_data = {
    annotation = "${var.vm_description}"
    memsize    = "${var.memory}"
    numvcpus   = "${var.cpus}"
  }
  vmx_data_post = {
    "ethernet0.connectiontype" = "${var.vmx_post_connectiontype}"
  }
}

build {
  sources = ["source.hyperv-iso.hyperv", "source.virtualbox-iso.vbox", "source.vmware-iso.vmware"]

  provisioner "file" {
    destination = "/tmp"
    source      = "data"
  }

  provisioner "file" {
    destination = "/tmp"
    source      = "installers"
  }

  provisioner "file" {
    destination = "/tmp"
    source      = "scripts"
  }

  provisioner "shell" {
    environment_vars = ["OTC_APPLIANCE_VERSION=${var.appliance_version}", "MYSQL_OTC_USER=${var.otc_manager_database_user}", "MYSQL_OTC_PWD=${var.otc_manager_database_pass}", "OTC_DEFAULT_PASS=${var.otc_manager_default_pass}", "OTC_INSTALL_HOME=${var.otc_manager_install_home}", "OTC_INSTALL_PATH=${var.otc_manager_install_path}", "http_proxy=${var.http_proxy}", "https_proxy=${var.https_proxy}", "no_proxy=${var.no_proxy}"]
    execute_command  = "echo ${var.ssh_pass} | {{ .Vars }} sudo -S -E bash '{{ .Path }}'"
    scripts          = ["scripts/networking.sh", "scripts/jre-oracle-8.sh", "scripts/mysql.sh", "scripts/openthinclient-installer.sh", "scripts/openthinclient-custom.sh", "scripts/openthinclient-gui.sh", "scripts/vmtools.sh", "scripts/motd.sh", "scripts/print-server.sh", "scripts/openthinclient-cleaner.sh", "scripts/minimize.sh"]
  }

  post-processor "vagrant" {
    keep_input_artifact = true
    output              = "builds/${var.hostname}.<no value>.box"
  }
}
