import pytest
import re

# set some default variables

ssh_name = "openthinclient"
ssh_pass = "0pen%TC"
otc_manager_database_user = "openthinclient"
otc_manager_database_pass = "openthinclient"

otc_manager_default_pass = "0pen%TC"
otc_manager_install_home = "/home/openthinclient/otc-manager-home/"


@pytest.mark.parametrize("name,version", [
    ("mysql-server", "5.5"),
    ("python", "2.7"),
    ("vim", "2:8"),
    ("zerofree", "1.0"),
    ("openssh-server", "1:7"),
    ("ntp", "1:4"),
    ("acpid", "1:2"),
    ("aptitude", "0.8"),
    ("sudo", "1.8"),
    ("bzip2", "1.0"),
    ("rsync", "3.1"),
    ("ldapscripts", "2.0"),
    ("htop", "2.0"),
    ("mc", "3:4"),
    ("vim", ""),
    ("screen", "4.5"),
    ("tcpdump", "4.9"),
    ("emacs", "46.1"),
    ("net-tools", "1.60"),
    ("dirmngr", "2.1"),
    ("network-manager", "1.6"),
    ("virt-what", "1.15" ),
    ("dos2unix", "7.3" )
])
def test_basic_packages_installed(host, name, version):
    pkg = host.package(name)
    assert pkg.is_installed
    assert pkg.version.startswith(version)


@pytest.mark.parametrize("name,version", [
    ("xtightvncviewer", "1:1.3"),
    ("dconf-tools", "0.26"),
    ("xserver-xorg", "1:7"),
    ("gnome-system-tools", "3.0"),
    ("firefox-esr", "68"),
    ("pluma", "1.16"),
    ("mate-desktop-environment-core", "1.16"),
    ("lightdm", "1.18"),
    ("network-manager-gnome", "1.4"),
    ("arandr", "0.1"),
])
def test_gui_packages_installed(host, name, version):
    pkg = host.package(name)
    assert pkg.is_installed
    assert pkg.version.startswith(version)


@pytest.mark.parametrize("user", [
    "root",
    "openthinclient",
])
def test_user_in_passwd_file(host, user):
    passwd = host.file("/etc/passwd")
    assert passwd.contains(user)


@pytest.mark.parametrize("service_name", [
    "lightdm",
    "mariadb",
])
def test_service_running(host, service_name):
    service = host.service(service_name)
    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize("proto,hostname,port", [
    ("tcp", "127.0.0.1", "3306"),
    ("tcp", "0.0.0.0", "22"),
    ("tcp", "::", "22"),
])
def test_socket_listening(host, proto, hostname, port):
    socketoptions = "{0}://{1}:{2}".format(proto, hostname, port)
    socket = host.socket(socketoptions)
    assert socket.is_listening


def test_passwd_file(host):
    passwd = host.file("/etc/passwd")
    assert passwd.contains("root")
    assert passwd.user == "root"
    assert passwd.group == "root"
    assert passwd.mode == 0o644


def test_openthinclient_user(host):
    user = host.user(ssh_name)
    assert user.name == ssh_name
    assert user.group == ssh_name
    assert user.exists is True


@pytest.mark.parametrize("filename", [
    "/usr/local/sbin/openthinclient-changepassword",
    "/usr/local/sbin/openthinclient-cleaner",
    "/usr/local/sbin/openthinclient-edit-sources-lst-lite",
    "/usr/local/sbin/openthinclient-ldapbackup",
    "/usr/local/sbin/openthinclient-restart",
    "/usr/local/sbin/zerofree.sh",
])
def test_otc_usr_local_sbin_files(host, filename):
    file = host.file(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists is True


@pytest.mark.parametrize("filename", [
    "/usr/local/bin/openthinclient-manager",
    "/usr/local/bin/openthinclient-vmversion",
])
def test_otc_usr_local_bin_files(host, filename):
    file = host.file(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists is True


@pytest.mark.parametrize("filename", [
    "/usr/local/sbin/openthinclient-changepassword",
    "/usr/local/sbin/openthinclient-cleaner",
    "/usr/local/sbin/openthinclient-edit-sources-lst-lite",
    "/usr/local/sbin/openthinclient-ldapbackup",
    "/usr/local/sbin/openthinclient-restart",
    "/usr/local/sbin/zerofree.sh",
])
def test_otc_usr_local_sbin_files(host, filename):
    file = host.file(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists is True


def test_crond_ldap_backup_file(host):
    managerbin = host.file("/etc/cron.d/openthinclient_ldap_backup")
    assert managerbin.user == "root"
    assert managerbin.group == "root"
    assert managerbin.exists is True


@pytest.mark.parametrize("filename,content", [
    ("/etc/sudoers.d/90-openthinclient-appliance", "openthinclient ALL=(ALL) NOPASSWD:ALL"),
])
def test_sudoers_file(host, filename, content):
    filen = host.file(filename)
    with host.sudo():
        host.check_output("whoami")
        assert filen.contains(content)
        assert filen.user == "root"
        assert filen.group == "root"
        assert filen.exists is True


@pytest.mark.parametrize("filename,content", [
    ("/usr/local/share/openthinclient/openthinclient-vm-version", "Operating system"),
])
def test_openthinclient_version_information_file_present(host, filename, content):
    filen = host.file(filename)
    with host.sudo():
        assert filen.contains(content)
        assert filen.user == "root"
        assert filen.group == "staff"
        assert filen.exists is True


@pytest.mark.parametrize("filename,content", [
    ("/etc/network/interfaces", "auto eth0"),
    ("/etc/network/interfaces", "iface eth0 inet dhcp"),
])
def test_for_eth0_in_etc_network_interfaces_file(host, filename, content):
    filen = host.file(filename)
    with host.sudo():
        assert filen.contains(content)
        assert filen.user == "root"
        assert filen.group == "root"
        assert filen.exists is True


def test_udev_rule_eth0_rules_file_workaround(host):
    directory = host.file("/etc/udev/rules.d/80-net-setup-link.rules")
    assert directory.user == "root"
    assert directory.group == "root"
    assert directory.is_symlink is True
    assert directory.linked_to == "/dev/null"


@pytest.mark.parametrize("filename,content", [
    ("/home/openthinclient/.bash_aliases", "alias ll='ls -l'"),
    ("/root/.bash_aliases", "alias ll='ls -l'"),
    ("/home/openthinclient/.bashrc", ". ~/.bash_aliases"),
    ("/root/.bashrc", ". ~/.bash_aliases"),
])
def test_bash_aliases_file(host, filename, content):
    with host.sudo():
        file = host.file(filename)
        assert file.contains(content)
        assert file.exists is True


@pytest.mark.parametrize("filename", [
    "/etc/X11/Xsession.d/21-lightdm-locale-fix",
])
def test_otc_gui_lightdm_locale_fix(host, filename):
    file = host.file(filename)
    assert file.user == "root"
    assert file.group == "root"
    assert file.exists is True
    # assert file.mode == 0o744 # FIXME - check if this needs to executable


@pytest.mark.parametrize("filename", [
    "/etc/lightdm/lightdm.conf",
])
def test_lightdm_config_file(host, filename):
    file = host.file(filename)
    # assert file.user == "root"
    # assert file.group == "root"
    assert file.exists is True


@pytest.mark.parametrize("filename,content", [
    ("/etc/lightdm/lightdm.conf", "greeter-setup-script=/usr/local/bin/openthinclient-default-user-fix"),
    ("/etc/lightdm/lightdm.conf", "allow-guest=false"),
    ("/etc/lightdm/lightdm.conf", "greeter-hide-users=false"),
    ("/etc/lightdm/lightdm.conf", "greeter-show-manual-login=true"),
])
def test_lightdm_config_content(host, filename, content):
    file = host.file(filename)
    assert file.contains(content)
    # assert file.group == "root"
    assert file.exists is True


@pytest.mark.parametrize("filename,content", [
    ("/etc/lightdm/lightdm-gtk-greeter.conf",
     "background=/usr/local/share/openthinclient/backgrounds/2019_1_magenta_2560x1440.jpg"),
    ("/etc/lightdm/lightdm-gtk-greeter.conf", "show-clock=true"),
])
def test_lightdm_config_content(host, filename, content):
    file = host.file(filename)
    assert file.contains(content)
    assert file.exists is True


@pytest.mark.parametrize("filename", [
    "/usr/local/bin/openthinclient-default-user-fix",
    "/usr/local/bin/openthinclient-keyboard-layout-fix",
    "/home/openthinclient/.config/autostart/keyboard-layout-fix.desktop",
])
def test_otc_gui_fixes_via_script(host, filename):
    filen = host.file(filename)
    assert filen.user == "openthinclient"
    assert filen.group == "openthinclient"
    assert filen.exists is True


@pytest.mark.parametrize("filename", [
    "/home/openthinclient/Desktop/change password.desktop",
    "/home/openthinclient/Desktop/livesupport.levigo.de.desktop",
    "/home/openthinclient/Desktop/mate-network-properties.desktop",
    "/home/openthinclient/Desktop/nm-connection-editor.desktop",
    "/home/openthinclient/Desktop/time.desktop",
    "/home/openthinclient/Desktop/openthinclient Manager WebConsole.desktop",
    "/home/openthinclient/Desktop/openthinclient service restart.desktop",
    "/home/openthinclient/Desktop/Oracle-Java-Licence",
    "/home/openthinclient/Desktop/README.desktop",
    "/home/openthinclient/Desktop/VNC Viewer.desktop",
])
def test_otc_desktop_icons_present(host, filename):
    file = host.file(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists is True


@pytest.mark.parametrize("filename", [
    "/home/openthinclient/Desktop/Version-Information.desktop",
    "/home/openthinclient/Desktop/openthinclient Legacy WebStart Manager.desktop",
    "/home/openthinclient/Desktop/Feature Bid.desktop",
    "/home/openthinclient/Desktop/Buy hardware.desktop",
    "/home/openthinclient/Desktop/professional support & hardware.desktop",
])
def test_otc_desktop_icons_not_present(host, filename):
    file = host.file(filename)
    assert file.exists is False


@pytest.mark.parametrize("filename", [
    "/usr/local/share/openthinclient/backgrounds/2019_1_magenta_2560x1440.jpg",
    "/usr/local/share/openthinclient/backgrounds/2019_1_beta_magenta_2560x1440.jpg",
    "/usr/local/share/openthinclient/backgrounds/desktopB_1920x1200.png",
    "/usr/local/share/openthinclient/backgrounds/OTC_VM_1280x1024.png",
    "/usr/local/share/openthinclient/icons/openthinclient_advisor.png",
    "/usr/local/share/openthinclient/icons/openthinclient_ceres_version.png",
    "/usr/local/share/openthinclient/icons/openthinclient_consus_version.png",
    "/usr/local/share/openthinclient/icons/openthinclient-features.png",
    "/usr/local/share/openthinclient/icons/openthinclient_manager.png",
    "/usr/local/share/openthinclient/icons/openthinclient_minerva_version.png",
    "/usr/local/share/openthinclient/icons/openthinclient_pales_version.png",
    "/usr/local/share/openthinclient/icons/openthinclient_professional_support.png",
    "/usr/local/share/openthinclient/icons/openthinclient_readme.png",
    "/usr/local/share/openthinclient/icons/openthinclient_service_restart.png",
    "/usr/local/share/openthinclient/icons/openthinclient_shop.png",
])
def test_otc_background_and_icons_present(host, filename):
    file = host.file(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists is True


@pytest.mark.parametrize("filename", [
    "/usr/local/share/openthinclient/documentation/README.txt",
    "/usr/local/share/openthinclient/documentation/README-openthinclient-VirtualAppliance.pdf",
])
def test_otc_documentation_present(host, filename):
    file = host.file(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists is True


@pytest.mark.parametrize("name", [
    "rpcbind",
])
def test_package_cleanup(host, name):
    assert host.package(name).is_installed == False


def test_basic_system_information(host):
    assert host.system_info.type == "linux"
    assert host.system_info.distribution == "debian"
    assert host.system_info.codename == "stretch"


@pytest.mark.parametrize("executable,expected_output", [
    ("/usr/bin/java -version", "1.8.0_202"),
])
def test_java_version(executable, expected_output, host):
    with host.sudo():
        cmd = host.run(executable)
        reported_version = re.findall('java version "(.+)"', cmd.stderr)
        assert reported_version[0] == expected_output


@pytest.mark.parametrize("executable,expected_output", [
    ("/usr/bin/java -version", "1.8.0"),
])
def test_java_major_version(executable, expected_output, host):
    with host.sudo():
        cmd = host.run(executable)
        reported_version = re.findall('java version "(.+)_\d{3}"', cmd.stderr)
        assert reported_version[0] == expected_output


@pytest.mark.parametrize("sysctl_option,expected_output", [
    ("kernel.hostname", "openthinclient-server"),
    ("vm.swappiness", 60),

])
def test_sysctl_values(sysctl_option, expected_output, host):
    with host.sudo():
        current_value = host.sysctl(sysctl_option)
        assert current_value == expected_output


@pytest.mark.parametrize("executable,expected_output", [
    ("dbus-launch gsettings get org.mate.background picture-filename",
     "'/usr/local/share/openthinclient/backgrounds/2019_1_magenta_2560x1440.jpg'\n"),
])
def test_mate_desktop_settings(executable, expected_output, host):
    cmd = host.run(executable)
    assert cmd.stdout == expected_output


@pytest.mark.parametrize("executable,expected_output", [
    ("df / | tail -1 | awk '{print $5}'",
     '50%'),
])
def test_free_diskspace(executable, expected_output, host):
    cmd = host.run(executable)
    avail = int(cmd.stdout.replace('%', ''))
    max = int(expected_output.replace('%', ''))
    use_limit_reached = False
    if avail > max:
        use_limit_reached = True
    assert use_limit_reached is False

@pytest.mark.parametrize("executable,expected_output", [
    ("dos2unix -ic /etc/vim/vimrc", ""),
    ("dos2unix -ic /etc/sudoers.d/90-openthinclient-appliance", ""),
])
def test_modified_system_file_linux_mode(executable, expected_output, host):
    with host.sudo():
        cmd = host.run_test(executable)
        assert cmd.stdout == expected_output

