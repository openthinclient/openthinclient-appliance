
variable "appliance_version" {
  type    = string
  default = "2022.1.4"
}

variable "vm_description" {
  type    = string
  default = "openthinclient is a Free Open Source Thin Client Solution consisting of a Linux based operating system along with a comprehensive Java based management GUI and server component. It is intended for environments where a medium to large number of Thin Clients must be supported and managed efficiently. Offering flexibility unheard of in the world of proprietary Thin Client Solutions, openthinclient empowers developers and integrators to create advanced Thin Client solutions... for free. www.openthinclient.org"
}

variable "vm_name" {
  type    = string
  default = "openthinclient-Appliance-2022.1.4"
}

variable "headless" {
  type    = string
  default = "true"
}

variable "cpus" {
  type    = string
  default = "2"
}

variable "memory" {
  type    = string
  default = "4096"
}

variable "disk_size" {
  type    = string
  default = "20480"
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

variable "port_max" {
  type    = string
  default = "9001"
}

variable "port_min" {
  type    = string
  default = "9001"
}

variable "dir" {
  type    = string
  default = "debian"
}

variable "iso_checksum" {
  type    = string
  default = "b462643a7a1b51222cd4a569dad6051f897e815d10aa7e42b68adc8d340932d861744b5ea14794daa5cc0ccfa48c51d248eda63f150f8845e8055d0a5d7e58e6"
}

variable "iso_url" {
  type    = string
  default = "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.0.0-amd64-netinst.iso"
}

variable "nodejs_checksum" {
  type    = string
  default = "fae6b7b88242c5a160b04b133aaf61b4ab9dae9af7fdf6bdc5ab4a7c700f56a32e475773117824ba95bc855f281f260453c031901f3f30ab023b9b82b72ad831"
}

variable "nodejs_url" {
  type    = string
  default = "https://nodejs.org/dist/v18.14.0/node-v18.14.0-linux-x64.tar.xz"
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

variable "ssh_timeout" {
  type    = string
  default = "60m"
}

variable "virtualbox_guest_os_type" {
  type    = string
  default = "Debian_64"
}

variable "virtualbox_hardware_clock" {
  type    = string
  default = "on"
}

variable "virtualbox_gpu_controller" {
  type    = string
  default = "vmsvga"
}

variable "virtualbox_network_type" {
  type    = string
  default = "bridged"
}

variable "virtualbox_bridge_adapter" {
  type    = string
  default = "Please choose your physical network interface!"
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
  boot_command       = [
  "c",
  "linux /install.amd/vmlinuz ",
  "auto ",
  "locale=en_US.UTF-8 ",
  "country=US ",
  "language=en ",
  "keymap=us ",
  "url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/preseed_hypv.cfg ",
  "hostname=${var.hostname} ",
  "domain=${var.hostname} ",
  "interface=auto ",
  "vga=788 noprompt ---<enter>",
  "initrd /install.amd/initrd.gz<enter>",
  "boot<enter>"
  ]
  vm_name            = "${var.vm_name}"
  headless           = "${var.headless}"
  cpus               = "${var.cpus}"
  memory             = "${var.memory}"
  disk_size          = "${var.disk_size}"
  iso_checksum       = "${var.iso_checksum}"
  iso_url            = "${var.iso_url}"
  http_directory     = "${var.dir}"
  http_port_max      = "${var.port_max}"
  http_port_min      = "${var.port_min}"
  ssh_username       = "${var.ssh_name}"
  ssh_password       = "${var.ssh_pass}"
  ssh_timeout        = "${var.ssh_timeout}"
  shutdown_command   = "echo ${var.ssh_pass} | sudo -S shutdown -P now"
  output_directory   = "builds/${var.vm_name}-hyperv"

  enable_secure_boot = false
  generation         = 2
  disk_block_size    = 1
}

source "virtualbox-iso" "vbox" {
  boot_command        = [
  "<esc><wait>",
  "install <wait>",
  "preseed/url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/preseed_vmbx.cfg ",
  "debian-installer=en_US auto locale=en_US kbd-chooser/method=us ",
  "keyboard-configuration/xkb-keymap=us <wait>",
  "netcfg/get_hostname=${var.hostname} <wait>",
  "netcfg/get_domain=${var.hostname} <wait>",
  "fb=false debconf/frontend=noninteractive ",
  "keyboard-configuration/modelcode=SKIP keyboard-configuration/layout=USA ",
  "keyboard-configuration/variant=USA console-setup/ask_detect=false ",
  "<enter><wait>"
  ]
  vm_name             = "${var.vm_name}"
  headless            = "${var.headless}"
  cpus                = "${var.cpus}"
  memory              = "${var.memory}"
  disk_size           = "${var.disk_size}"
  iso_checksum        = "${var.iso_checksum}"
  iso_url             = "${var.iso_url}"
  http_directory      = "${var.dir}"
  http_port_max       = "${var.port_max}"
  http_port_min       = "${var.port_min}"
  ssh_password        = "${var.ssh_pass}"
  ssh_username        = "${var.ssh_name}"
  ssh_wait_timeout    = "${var.ssh_timeout}"
  shutdown_command    = "echo ${var.ssh_pass} | sudo -S shutdown -P now"
  output_directory    = "builds/${var.vm_name}-virtualbox"

  guest_os_type       = "${var.virtualbox_guest_os_type}"
  post_shutdown_delay = "30s"
  vboxmanage          = [
    ["modifyvm", "{{ .Name }}", "--vram", "32"],
    ["modifyvm", "{{ .Name }}", "--description", "${var.vm_description}"]
    ]
  vboxmanage_post     = [
    ["modifyvm", "{{ .Name }}", "--vram", "32"],
    ["modifyvm", "{{ .Name }}", "--rtcuseutc", "${var.virtualbox_hardware_clock}"],
    ["modifyvm", "{{ .Name }}", "--graphicscontroller", "${var.virtualbox_gpu_controller}"],
    ["modifyvm", "{{ .Name }}", "--nic1", "${var.virtualbox_network_type}"],
    ["modifyvm", "{{ .Name }}", "--bridgeadapter1", "${var.virtualbox_bridge_adapter}"]
    ]
}

source "vmware-iso" "vmware" {
  boot_command     = [
  "<esc><wait>",
  "install <wait>",
  "preseed/url=http://{{ .HTTPIP }}:{{ .HTTPPort }}/preseed_vmbx.cfg ",
  "debian-installer=en_US auto locale=en_US kbd-chooser/method=us ",
  "keyboard-configuration/xkb-keymap=us <wait>",
  "netcfg/get_hostname=${var.hostname} <wait>",
  "netcfg/get_domain=${var.hostname} <wait>",
  "fb=false debconf/frontend=noninteractive ",
  "keyboard-configuration/modelcode=SKIP keyboard-configuration/layout=USA ",
  "keyboard-configuration/variant=USA console-setup/ask_detect=false ",
  "<enter><wait>"
  ]
  vm_name          = "${var.vm_name}"
  headless         = "${var.headless}"
  cpus             = "${var.cpus}"
  memory           = "${var.memory}"
  disk_size        = "${var.disk_size}"
  iso_checksum     = "${var.iso_checksum}"
  iso_url          = "${var.iso_url}"
  http_directory   = "${var.dir}"
  http_port_max    = "${var.port_max}"
  http_port_min    = "${var.port_min}"
  ssh_password     = "${var.ssh_pass}"
  ssh_username     = "${var.ssh_name}"
  ssh_wait_timeout = "${var.ssh_timeout}"
  shutdown_command = "echo ${var.ssh_pass} | sudo -S shutdown -P now"
  output_directory = "builds/${var.vm_name}-vmware"

  guest_os_type    = "${var.vmware_guest_os_type}"
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
    environment_vars = [
      "OTC_APPLIANCE_VERSION=${var.appliance_version}",
      "MYSQL_OTC_USER=${var.otc_manager_database_user}",
      "MYSQL_OTC_PWD=${var.otc_manager_database_pass}",
      "OTC_DEFAULT_PASS=${var.otc_manager_default_pass}",
      "OTC_INSTALL_HOME=${var.otc_manager_install_home}",
      "OTC_INSTALL_PATH=${var.otc_manager_install_path}",
      "NODEJS_URL=${var.nodejs_url}",
      "NODEJS_CHECKSUM=${var.nodejs_checksum}",
      "http_proxy=${var.http_proxy}",
      "https_proxy=${var.https_proxy}",
      "no_proxy=${var.no_proxy}"
    ]
    execute_command  = "echo ${var.ssh_pass} | {{ .Vars }} sudo -S -E bash '{{ .Path }}'"
    scripts          = [
      "scripts/networking.sh",
      "scripts/openthinclient-installer.sh",
      "scripts/openthinclient-custom.sh",
      "scripts/openthinclient-gui.sh",
      "scripts/vmtools.sh",
      "scripts/motd.sh",
      "scripts/print-server.sh",
      "scripts/openthinclient-cleaner.sh",
      "scripts/minimize.sh"
    ]
  }

  post-processor "vagrant" {
    keep_input_artifact = true
    output              = "builds/${var.hostname}.{{.Provider}}.box"
  }
}
