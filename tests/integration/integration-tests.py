import pytest
import re

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
def test_basic_packages_installed(Package, name, version):
    assert Package(name).is_installed
    assert Package(name).version.startswith(version)


@pytest.mark.parametrize("name,version", [
    ("xtightvncviewer", "1.3"),
    ("dconf-tools", "0.22"),
    ("xserver-xorg", "1.7"),
    ("mate-system-tools", "1.8"),
    ("iceweasel", "45"),
    ("pluma", "1.8"),
])
def test_gui_packages_installed(Package, name, version):
    assert Package(name).is_installed
    assert Package(name).version.startswith(version)


@pytest.mark.parametrize("user", [
    ("root"),
    ("openthinclient"),
])

def test_user_in_passwd_file(File, user):
    passwd = File("/etc/passwd")
    assert passwd.contains(user)


@pytest.mark.parametrize("service_name", [
    ("openthinclient-manager"),
    ("lightdm"),
    ("mysql"),
])

def test_service_running(Service, service_name):
    service = Service(service_name)
    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize("proto,host,port", [
    ("tcp", "127.0.0.1", "3306"),
    ("tcp", "0.0.0.0","22"),
])

def test_socket_listening(Socket, proto, host, port):
    socketoptions = "{0}://{1}:{2}".format(proto, host, port)
    socket = Socket(socketoptions)
    assert socket.is_listening


def test_passwd_file(File):
    passwd = File("/etc/passwd")
    assert passwd.contains("root")
    assert passwd.user == "root"
    assert passwd.group == "root"
    assert passwd.mode == 0o644

def test_openthinclient_user(User):
    user = User("openthinclient")
    assert user.name == "openthinclient"
    assert user.group == "openthinclient"
    assert user.exists == True


def test_openthinclient_manager_file(File):
    managerbin = File("/opt/openthinclient/bin/openthinclient-manager")
    assert managerbin.user == "root"
    assert managerbin.group == "root"
    assert managerbin.exists == True


def test_openthinclient_install_directory(File):
    dir = File("/opt/openthinclient/")
    assert dir.user == "root"
    assert dir.group == "root"
    assert dir.is_directory == True

def test_openthinclient_home_directory(File):
    dir = File("/home/openthinclient/otc-manager-home/")
    assert dir.user == "root"
    assert dir.group == "root"
    assert dir.is_directory == True


@pytest.mark.parametrize("filename", [
    ("/usr/local/bin/openthinclient-manager"),
    ("/usr/local/bin/openthinclient-vmversion"),
])

def test_otc_usr_local_bin_files(File, filename):
    file = File(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists == True


@pytest.mark.parametrize("filename", [
    ("/usr/local/sbin/openthinclient-changepassword"),
    ("/usr/local/sbin/openthinclient-cleaner"),
    ("/usr/local/sbin/openthinclient-edit-sources-lst-lite"),
    ("/usr/local/sbin/openthinclient-ldapbackup"),
    ("/usr/local/sbin/openthinclient-restart"),
    ("/usr/local/sbin/zerofree.sh"),
])

def test_otc_usr_local_sbin_files(File, filename):
    file = File(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists == True

def test_crond_ldap_backup_file(File):
    managerbin = File("/etc/cron.d/openthinclient_ldap_backup")
    assert managerbin.user == "root"
    assert managerbin.group == "root"
    assert managerbin.exists == True


@pytest.mark.parametrize("filename,content", [
    ("/etc/sudoers.d/90-openthinclient-appliance", "openthinclient ALL=(ALL) NOPASSWD:ALL"),
])

def test_sudoers_file(File, filename, content, Command, Sudo):
    file = File(filename)
    with Sudo():
        Command.check_output("whoami")
        assert file.contains(content)
        assert file.user == "root"
        assert file.group == "root"
        assert file.exists == True


@pytest.mark.parametrize("filename", [
    ("/etc/X11/Xsession.d/21-lightdm-locale-fix"),
])

def test_otc_gui_lightdm_locale_fix(File, filename):
    file = File(filename)
    assert file.user == "root"
    assert file.group == "root"
    assert file.exists == True
    # assert file.mode == 0o744 # FIXME - check if this needs to executable


@pytest.mark.parametrize("filename", [
    ("/etc/lightdm/lightdm.conf"),
])

def test_lightdm_config_file(File, filename):
    file = File(filename)
    #assert file.user == "root"
    #assert file.group == "root"
    assert file.exists == True



@pytest.mark.parametrize("filename,content", [
    ("/etc/lightdm/lightdm.conf", "greeter-setup-script=/usr/local/bin/openthinclient-default-user-fix" ),
    ("/etc/lightdm/lightdm.conf", "allow-guest=false"),
    ("/etc/lightdm/lightdm.conf", "greeter-hide-users=false"),
    ("/etc/lightdm/lightdm.conf", "greeter-show-manual-login=true"),
])

def test_lightdm_config_content(File, filename, content):
    file = File(filename)
    assert file.contains(content)
    #assert file.group == "root"
    assert file.exists == True


@pytest.mark.parametrize("filename,content", [
    ("/etc/lightdm/lightdm-gtk-greeter.conf",
        "background=/usr/local/share/openthinclient/backgrounds/openthinclient-server-Desktop-Pales.jpg" ),
    ("/etc/lightdm/lightdm-gtk-greeter.conf", "show-clock=true"),
])

def test_lightdm_config_content(File, filename, content):
    file = File(filename)
    assert file.contains(content)
    #assert file.group == "root"
    assert file.exists == True


@pytest.mark.parametrize("filename", [
    ("/usr/local/bin/openthinclient-default-user-fix"),
    ("/usr/local/bin/openthinclient-keyboard-layout-fix"),
    ("/home/openthinclient/.config/autostart/keyboard-layout-fix.desktop"),
])

def test_otc_gui_fixes_via_script(File, filename):
    file = File(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists == True


@pytest.mark.parametrize("filename", [
    ("/home/openthinclient/Desktop/Buy hardware.desktop"),
    ("/home/openthinclient/Desktop/change password.desktop"),
    #("/home/openthinclient/Desktop/Edit openthinclient package sources.desktop"),
    ("/home/openthinclient/Desktop/Feature Bid.desktop"),
    ("/home/openthinclient/Desktop/livesupport.levigo.de.desktop"),
    ("/home/openthinclient/Desktop/mate-network-properties.desktop"),
    ("/home/openthinclient/Desktop/mate-time.desktop"),
    ("/home/openthinclient/Desktop/openthinclient Manager.desktop"),
    ("/home/openthinclient/Desktop/openthinclient Package Manager.desktop"),
    ("/home/openthinclient/Desktop/openthinclient service restart.desktop"),
    ("/home/openthinclient/Desktop/Oracle-Java-Licence"),
    ("/home/openthinclient/Desktop/professional support & hardware.desktop"),
    ("/home/openthinclient/Desktop/README.desktop"),
    #("/home/openthinclient/Desktop/teamviewer-teamviewer9.desktop"),
    ("/home/openthinclient/Desktop/Version-Information.desktop"),
    ("/home/openthinclient/Desktop/VNC Viewer.desktop"),
])

def test_otc_desktop_icons(File, filename):
    file = File(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists == True


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

def test_otc_background_and_icons(File, filename):
    file = File(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists == True


@pytest.mark.parametrize("filename", [
    ("/usr/local/share/openthinclient/documentation/README.txt"),
    ("/usr/local/share/openthinclient/documentation/README-openthinclient-VirtualAppliance.pdf"),
])

def test_otc_documentation(File, filename):
    file = File(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists == True

@pytest.mark.parametrize("name,version", [
    ("mate-desktop-environment-core", "1.8"),
    ("lightdm", "1.10"),
])

def test_gui_packages_installed(Package, name, version):
    assert Package(name).is_installed
    assert Package(name).version.startswith(version)


@pytest.mark.parametrize("name", [
    ("rpcbind"),
])
def test_package_cleanup(Package, name):
    assert Package(name).is_installed == False


def test_basic_system_information(SystemInfo):
    assert SystemInfo.type == "linux"
    assert SystemInfo.distribution == "debian"
    assert SystemInfo.codename == "jessie"


"""
@pytest.mark.parametrize("executable,expected_output", [
    ("/usr/bin/java -version", 'java version "1.8.0_131"\nJava(TM) SE Runtime Environment (build 1.8.0_131-b11)\nJava HotSpot(TM) Client VM (build 25.131-b11, mixed mode)\n'),
])

def test_java_version_full_output(executable, expected_output, Command, Sudo):
    with Sudo():
        cmd = Command(executable)
        # output = cmd.stdout
        assert cmd.stderr == expected_output
"""

@pytest.mark.parametrize("executable,expected_output", [
    ("/usr/bin/java -version", "1.8.0_144"),
])
def test_java_version(executable, expected_output, Command, Sudo):
    with Sudo():
        cmd = Command(executable)
        reported_version = re.findall('java version "(.+)"', cmd.stderr)
        assert reported_version[0] == expected_output

@pytest.mark.parametrize("executable,expected_output", [
    ("/usr/bin/java -version", "1.8.0"),
])
def test_java_major_version(executable, expected_output, Command, Sudo):
    with Sudo():
        cmd = Command(executable)
        reported_version = re.findall('java version "(.+)_\d{3}"', cmd.stderr)
        assert reported_version[0] == expected_output

@pytest.mark.parametrize("sysctl_option,expected_output", [
    ("kernel.hostname", "openthinclient-server"),
    ("vm.swappiness", 60),

])

def test_sysctl_values(sysctl_option, expected_output, Sysctl, Sudo):
    with Sudo():
        current_value = Sysctl(sysctl_option)
        assert current_value == expected_output


@pytest.mark.parametrize("executable,expected_output", [
    ("dbus-launch gsettings get org.mate.background picture-filename",
     "'/usr/local/share/openthinclient/backgrounds/openthinclient-server-Desktop-Pales.jpg'\n"),
])

def test_mate_desktop_settings(executable, expected_output, Command):
        cmd = Command(executable)
        #output = cmd.stdout
        assert cmd.stdout == expected_output


@pytest.mark.parametrize("executable,expected_output", [
    ("mysql -uroot -proot -e 'use openthinclient;'", ""),
])
def test_if_openthinclient_mysql_db_exists(executable, expected_output, Command, Sudo):
    with Sudo():
        #cmd = Command(executable)
        cmd = Command.run_test(executable)
        assert cmd.exit_status == 0
        assert cmd.stderr == expected_output


@pytest.mark.parametrize("executable,expected_output", [
    ("mysql -uroot -proot -sse 'SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = \"openthinclient\")';", "1\n"),
])
def test_if_openthinclient_mysql_user_exists(executable, expected_output, Command, Sudo):
    with Sudo():
        # cmd = Command(executable)
        cmd = Command.run_test(executable)
        assert cmd.exit_status == 0
        assert cmd.stdout == expected_output


@pytest.mark.parametrize("executable,expected_output", [
    ("mysql -uopenthinclient -popenthinclient -e 'use openthinclient;'", ""),
])
def test_if_openthinclient_user_has_access_to_mysql_db(executable, expected_output, Command, Sudo):
    with Sudo():
        #cmd = Command(executable)
        cmd = Command.run_test(executable)
        assert cmd.exit_status == 0
        assert cmd.stderr == expected_output

@pytest.mark.parametrize("executable,expected_output", [
    ("ls -A /home/openthinclient/otc-manager-home/nfs/root/var/cache/archives/1/", ""),
])
def test_if_openthinclient_package_cache_dir_is_empty(executable, expected_output, Command, Sudo):
    with Sudo():
        #cmd = Command(executable)
        cmd = Command.run_test(executable)
        assert cmd.exit_status == 0
        assert cmd.stdout == expected_output