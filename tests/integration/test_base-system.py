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
    ("python3", ""),
    ("zerofree", ""),
    ("openssh-server", ""),
    ("ntp", ""),
    ("acpid", ""),
    ("aptitude", ""),
    ("sudo", ""),
    ("bzip2", ""),
    ("rsync", ""),
    ("ldapscripts", ""),
    ("htop", ""),
    ("mc", ""),
    ("vim", ""),
    ("screen", ""),
    ("tcpdump", ""),
    ("emacs", ""),
    ("net-tools", ""),
    ("dirmngr", ""),
    ("network-manager", ""),
    ("virt-what", ""),
    ("dos2unix", ""),
    ("dnsutils", ""),
    ("unattended-upgrades", ""),
])
def test_basic_packages_installed(host, name, version):
    pkg = host.package(name)
    assert pkg.is_installed
    assert pkg.version.startswith(version)


@pytest.mark.parametrize("name,version", [
    ("tigervnc-viewer", ""),
    ("dconf-cli", ""),
    ("dconf-editor", ""),
    ("xserver-xorg", ""),
    ("gnome-system-tools", ""),
    ("chromium", ""),
    ("pluma", ""),
    ("mate-desktop-environment-core", ""),
    ("lightdm", ""),
    ("network-manager-gnome", ""),
    ("arandr", ""),
    ("liblightdm-gobject-dev", ""),
    ("gir1.2-webkit2-4.0", ""),
    ("icedtea-netx", ""),
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
    "wizard-server",
    "unattended-upgrades"
])
def test_service_running(host, service_name):
    service = host.service(service_name)
    assert service.is_enabled
    assert service.is_running
    

@pytest.mark.parametrize("proto,hostname,port", [
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
    assert user.exists
    assert user.name == ssh_name
    assert user.group == ssh_name    


@pytest.mark.parametrize("filename", [
    "/usr/local/sbin/openthinclient-cleaner",
    "/usr/local/sbin/openthinclient-ldapbackup",
    "/usr/local/sbin/openthinclient-restart",
    "/usr/local/sbin/zerofree.sh",
])
def test_otc_usr_local_sbin_files(host, filename):
    file = host.file(filename)
    assert file.exists
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"


@pytest.mark.parametrize("filename", [
    "/usr/local/bin/openthinclient-caja-desktop-fix",
    "/usr/local/bin/openthinclient-greeter.py",
    "/usr/local/bin/openthinclient-vmversion",
    "/usr/local/bin/tcos-ascii",
    "/usr/local/bin/tcos-ip",
    "/usr/local/bin/tcos-reboot-required"
])
def test_otc_usr_local_bin_files(host, filename):
    file = host.file(filename)
    assert file.exists
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"


def test_crond_ldap_backup_file(host):
    managerbin = host.file("/etc/cron.d/openthinclient_ldap_backup")
    assert managerbin.exists
    assert managerbin.user == "root"
    assert managerbin.group == "root"



@pytest.mark.parametrize("filename,content", [
    ("/etc/sudoers.d/90-openthinclient-appliance", "openthinclient ALL=(ALL) NOPASSWD:ALL"),
])
def test_sudoers_file(host, filename, content):
    filen = host.file(filename)
    with host.sudo():
        host.check_output("whoami")
        assert filen.exists
        assert filen.contains(content)
        assert filen.user == "root"
        assert filen.group == "root"


@pytest.mark.parametrize("filename,content", [
    ("/usr/local/share/openthinclient/openthinclient-vm-version", "Operating system"),
])
def test_openthinclient_version_information_file_present(host, filename, content):
    filen = host.file(filename)
    with host.sudo():
        assert filen.exists
        assert filen.contains(content)
        assert filen.user == "root"
        assert filen.group == "root"


@pytest.mark.parametrize("filename,content", [
    ("/etc/network/interfaces", "auto eth0"),
    ("/etc/network/interfaces", "iface eth0 inet dhcp"),
])
def test_for_eth0_in_etc_network_interfaces_file(host, filename, content):
    filen = host.file(filename)
    with host.sudo():
        assert filen.exists
        assert filen.contains(content)
        assert filen.user == "root"
        assert filen.group == "root"


def test_udev_rule_eth0_rules_file_workaround(host):
    directory = host.file("/etc/udev/rules.d/80-net-setup-link.rules")
    assert directory.is_symlink
    assert directory.linked_to == "/dev/null"
    assert directory.user == "root"
    assert directory.group == "root"


@pytest.mark.parametrize("filename,content", [
    ("/home/openthinclient/.bash_aliases", "alias ll='ls -alF'"),
    ("/root/.bash_aliases", "alias ll='ls -alF'"),
    ("/home/openthinclient/.bashrc", ". ~/.bash_aliases"),
    ("/root/.bashrc", ". ~/.bash_aliases"),
    ("/home/openthinclient/.bash_profile", "source ~/.bashrc"),
])
def test_bash_aliases_file(host, filename, content):
    with host.sudo():
        file = host.file(filename)
        assert file.exists
        assert file.contains(content)


@pytest.mark.parametrize("filename", [
    "/etc/X11/Xsession.d/21-lightdm-locale-fix",
])
def test_otc_gui_lightdm_locale_fix(host, filename):
    file = host.file(filename)
    assert file.exists
    assert file.user == "root"
    assert file.group == "root"
    assert file.mode == 0o755

def test_ctrl_alt_del_reboot_keyboard_config_disabled(host):
    directory = host.file("/lib/systemd/system/ctrl-alt-del.target")
    assert directory.is_symlink
    assert directory.linked_to == "/dev/null"
    assert directory.user == "root"
    assert directory.group == "root"


@pytest.mark.parametrize("filename", [
    "/etc/lightdm/lightdm.conf",
])
def test_lightdm_config_file(host, filename):
    file = host.file(filename)
    assert file.exists


@pytest.mark.parametrize("filename,content", [
    ("/etc/lightdm/lightdm.conf", "greeter-session=lightdm-openthinclient-greeter"),
    ("/etc/lightdm/lightdm.conf", "allow-guest=false"),
    ("/etc/lightdm/lightdm.conf", "greeter-hide-users=false"),
    ("/etc/lightdm/lightdm.conf", "greeter-show-manual-login=true"),
])
def test_lightdm_config_content(host, filename, content):
    file = host.file(filename)
    assert file.exists
    assert file.contains(content)


@pytest.mark.parametrize("filename", [
    "/usr/local/bin/openthinclient-caja-desktop-fix",
    "/usr/local/bin/openthinclient-greeter.py",
    "/usr/local/bin/openthinclient-vmversion",
    "/usr/local/bin/tcos-ascii",
    "/usr/local/bin/tcos-ip",
    "/usr/local/bin/tcos-reboot-required",
])
def test_otc_gui_fixes_via_script(host, filename):
    filen = host.file(filename)
    assert filen.exists
    assert filen.mode == 0o755


@pytest.mark.parametrize("filename", [
    "/home/openthinclient/Desktop/otc_livesupport.desktop",
    "/home/openthinclient/Desktop/otc_manager_gui.desktop",
    "/home/openthinclient/Desktop/otc_service_restart.desktop",
    "/home/openthinclient/Desktop/otc_VA_README.desktop",
])  
def test_otc_desktop_icons_present(host, filename):
    file = host.file(filename)
    assert file.exists
    assert file.mode == 0o755


@pytest.mark.parametrize("filename", [
    "/usr/local/share/openthinclient/backgrounds/default.png",
    "/usr/local/share/openthinclient/icons/openthinclient_manager.png",
    "/usr/local/share/openthinclient/icons/openthinclient_professional_support.png",
    "/usr/local/share/openthinclient/icons/openthinclient_readme.png",
    "/usr/local/share/openthinclient/icons/openthinclient_service_restart.png",
])
def test_otc_background_and_icons_present(host, filename):
    file = host.file(filename)
    assert file.exists
    assert file.mode == 0o644


@pytest.mark.parametrize("name", [
    "rpcbind",
])
def test_package_cleanup(host, name):
    assert not host.package(name).is_installed


def test_basic_system_information(host):
    assert host.system_info.type == "linux"
    assert host.system_info.distribution == "debian"
    assert host.system_info.codename == "bullseye"


@pytest.mark.parametrize("executable,expected_output", [
    ("/usr/bin/java -version", "11."),
])
def test_java_version(executable, expected_output, host):
    with host.sudo():
        cmd = host.run(executable)
        reported_version = re.findall('openjdk version "(.+)"', cmd.stderr)
        assert reported_version[0].startswith(expected_output)


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
     "'/usr/local/share/openthinclient/backgrounds/default.png'\n"),
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


@pytest.mark.parametrize("executable, expected_output", [
    ("dos2unix -ic /etc/vim/vimrc", ""),
    ("dos2unix -ic /etc/sudoers.d/90-openthinclient-appliance", ""),
    ("dos2unix -ic /usr/local/sbin/zerofree.sh", ""),
    ("dos2unix -ic /usr/local/sbin/openthinclient*", ""),
    ("dos2unix -ic /usr/local/bin/openthinclient*", ""),
    ("dos2unix -ic /usr/local/bin/tcos*", ""),
])
def test_modified_system_file_linux_mode(executable, expected_output, host):
    with host.sudo():
        cmd = host.run_test(executable)
        assert cmd.stdout == expected_output


@pytest.mark.parametrize("path", [
    "/usr/local/sbin",
    "/usr/sbin",
    "/sbin"
])
def test_path_in_profile_file(host, path):
    profile = host.file("/home/openthinclient/.profile")
    assert profile.contains(path)


def test_openthinclient_user_dotxsessionrc(host):
    managerbin = host.file("/home/openthinclient/.xsessionrc")
    assert managerbin.exists
    assert managerbin.mode == 0o644
    assert managerbin.user == "openthinclient"
    assert managerbin.group == "openthinclient"


@pytest.mark.parametrize("setting", [
    "xset s off",
    "xset -dpms",
])
def test_xset_openthinclient_user_dotxsessionrc(host, setting):
    file = host.file("/home/openthinclient/.xsessionrc")
    assert file.contains(setting)


@pytest.mark.parametrize("limit, result", [
    ("-Hn", "65535"),
    ("-Sn", "65535"),
])
def test_limit(host, limit, result):
    with host.sudo():
        output = host.check_output('ulimit ' + limit)
        assert output == result


@pytest.mark.parametrize("limit, result", [
    ("-Hn", "65535"),
    ("-Sn", "65535"),
])
def test_limit_otc_user(host, limit, result):
    output = host.check_output('ulimit ' + limit)
    assert output == result
