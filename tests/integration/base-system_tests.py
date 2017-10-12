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
    ("vim", "2:7"),
    ("zerofree", "1.0"),
    ("openssh-server", "1:6"),
    ("oracle-java8-installer", "8"),
    ("oracle-java8-set-default", "8"),
    ("ntp", "1:4"),
    ("acpid", "1:2"),
    ("sudo", "1.8"),
    ("bzip2", "1.0"),
    ("rsync", "3.1"),
    ("ldapscripts", "2.0"),
    ("htop", "1.0"),

])
def test_basic_packages_installed(host, name, version):
    pkg = host.package(name)
    assert pkg.is_installed
    assert pkg.version.startswith(version)


@pytest.mark.parametrize("name,version", [
    ("xtightvncviewer", "1.3"),
    ("dconf-tools", "0.22"),
    ("xserver-xorg", "1.7"),
    ("mate-system-tools", "1.8"),
    ("iceweasel", "45"),
    ("pluma", "1.8"),
])
def test_gui_packages_installed(host, name, version):
    pkg = host.package(name)
    assert pkg.is_installed
    assert pkg.version.startswith(version)


@pytest.mark.parametrize("user", [
    ("root"),
    ("openthinclient"),
])

def test_user_in_passwd_file(host, user):
    passwd = host.file("/etc/passwd")
    assert passwd.contains(user)


@pytest.mark.parametrize("service_name", [
    ("lightdm"),
    ("mysql"),
])

def test_service_running(host, service_name):
    service = host.service(service_name)
    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize("proto,hostname,port", [
    ("tcp", "127.0.0.1", "3306"),
    ("tcp", "0.0.0.0","22"),
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
    ("/usr/local/sbin/openthinclient-changepassword"),
    ("/usr/local/sbin/openthinclient-cleaner"),
    ("/usr/local/sbin/openthinclient-edit-sources-lst-lite"),
    ("/usr/local/sbin/openthinclient-ldapbackup"),
    ("/usr/local/sbin/openthinclient-restart"),
    ("/usr/local/sbin/zerofree.sh"),
])

def test_otc_usr_local_sbin_files(host, filename):
    file = host.file(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists is True


@pytest.mark.parametrize("filename", [
    ("/usr/local/bin/openthinclient-manager"),
    ("/usr/local/bin/openthinclient-vmversion"),
])


def test_otc_usr_local_bin_files(host, filename):
    file = host.file(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists is True


@pytest.mark.parametrize("filename", [
    ("/usr/local/sbin/openthinclient-changepassword"),
    ("/usr/local/sbin/openthinclient-cleaner"),
    ("/usr/local/sbin/openthinclient-edit-sources-lst-lite"),
    ("/usr/local/sbin/openthinclient-ldapbackup"),
    ("/usr/local/sbin/openthinclient-restart"),
    ("/usr/local/sbin/zerofree.sh"),
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
    file = host.file(filename)
    with host.sudo():
        host.check_output("whoami")
        assert file.contains(content)
        assert file.user == "root"
        assert file.group == "root"
        assert file.exists is True

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
    ("/etc/X11/Xsession.d/21-lightdm-locale-fix"),
])

def test_otc_gui_lightdm_locale_fix(host, filename):
    file = host.file(filename)
    assert file.user == "root"
    assert file.group == "root"
    assert file.exists is True
    # assert file.mode == 0o744 # FIXME - check if this needs to executable


@pytest.mark.parametrize("filename", [
    ("/etc/lightdm/lightdm.conf"),
])

def test_lightdm_config_file(host, filename):
    file = host.file(filename)
    #assert file.user == "root"
    #assert file.group == "root"
    assert file.exists is True

@pytest.mark.parametrize("filename,content", [
    ("/etc/lightdm/lightdm.conf", "greeter-setup-script=/usr/local/bin/openthinclient-default-user-fix" ),
    ("/etc/lightdm/lightdm.conf", "allow-guest=false"),
    ("/etc/lightdm/lightdm.conf", "greeter-hide-users=false"),
    ("/etc/lightdm/lightdm.conf", "greeter-show-manual-login=true"),
])

def test_lightdm_config_content(host, filename, content):
    file = host.file(filename)
    assert file.contains(content)
    #assert file.group == "root"
    assert file.exists is True


@pytest.mark.parametrize("filename,content", [
    ("/etc/lightdm/lightdm-gtk-greeter.conf",
        "background=/usr/local/share/openthinclient/backgrounds/openthinclient-server-Desktop-Pales.jpg" ),
    ("/etc/lightdm/lightdm-gtk-greeter.conf", "show-clock=true"),
])

def test_lightdm_config_content(host, filename, content):
    file = host.file(filename)
    assert file.contains(content)
    #assert file.group == "root"
    assert file.exists is True


@pytest.mark.parametrize("filename", [
    ("/usr/local/bin/openthinclient-default-user-fix"),
    ("/usr/local/bin/openthinclient-keyboard-layout-fix"),
    ("/home/openthinclient/.config/autostart/keyboard-layout-fix.desktop"),
])

def test_otc_gui_fixes_via_script(host, filename):
    file = host.file(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists is True


@pytest.mark.parametrize("filename", [
    "/home/openthinclient/Desktop/Buy hardware.desktop",
    "/home/openthinclient/Desktop/change password.desktop",
    "/home/openthinclient/Desktop/Feature Bid.desktop",
    "/home/openthinclient/Desktop/livesupport.levigo.de.desktop",
    "/home/openthinclient/Desktop/mate-network-properties.desktop",
    "/home/openthinclient/Desktop/mate-time.desktop",
    "/home/openthinclient/Desktop/openthinclient Manager.desktop",
    "/home/openthinclient/Desktop/openthinclient Package Manager.desktop",
    "/home/openthinclient/Desktop/openthinclient service restart.desktop",
    "/home/openthinclient/Desktop/Oracle-Java-Licence",
    "/home/openthinclient/Desktop/professional support & hardware.desktop",
    "/home/openthinclient/Desktop/README.desktop",
    "/home/openthinclient/Desktop/Version-Information.desktop",
    "/home/openthinclient/Desktop/VNC Viewer.desktop",
])

def test_otc_desktop_icons(host, filename):
    file = host.file(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists is True


@pytest.mark.parametrize("filename", [
    ("/usr/local/share/openthinclient/backgrounds/openthinclient-server-Desktop-Pales.jpg"),
    ("/usr/local/share/openthinclient/backgrounds/desktopB_1920x1200.png"),
    ("/usr/local/share/openthinclient/backgrounds/OTC_VM_1280x1024.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_advisor.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_ceres_version.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_consus_version.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient-features.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_manager.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_minerva_version.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_pales_version.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_professional_support.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_readme.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_service_restart.png"),
    ("/usr/local/share/openthinclient/icons/openthinclient_shop.png"),
])

def test_otc_background_and_icons(host, filename):
    file = host.file(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists is True


@pytest.mark.parametrize("filename", [
    ("/usr/local/share/openthinclient/documentation/README.txt"),
    ("/usr/local/share/openthinclient/documentation/README-openthinclient-VirtualAppliance.pdf"),
])

def test_otc_documentation(host, filename):
    file = host.file(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists is True

@pytest.mark.parametrize("name,version", [
    ("mate-desktop-environment-core", "1.8"),
    ("lightdm", "1.10"),
])

def test_gui_packages_installed(host, name, version):
    assert host.package(name).is_installed
    assert host.package(name).version.startswith(version)


@pytest.mark.parametrize("name", [
    ("rpcbind"),
])
def test_package_cleanup(host, name):
    assert host.package(name).is_installed == False


def test_basic_system_information(host):
    assert host.system_info.type == "linux"
    assert host.system_info.distribution == "debian"
    assert host.system_info.codename == "jessie"


@pytest.mark.parametrize("executable,expected_output", [
    ("/usr/bin/java -version", "1.8.0_144"),
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
     "'/usr/local/share/openthinclient/backgrounds/openthinclient-server-Desktop-Pales.jpg'\n"),
])

def test_mate_desktop_settings(executable, expected_output, host):
        cmd = host.run(executable)
        assert cmd.stdout == expected_output
