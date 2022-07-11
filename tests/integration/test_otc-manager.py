import pytest
import re
import time

# set some default variables

ssh_name = "openthinclient"
ssh_pass = "0pen%TC"
otc_manager_database_user = "openthinclient"
otc_manager_database_pass = "openthinclient"

otc_manager_default_pass = "0pen%TC"
otc_manager_install_home = "/home/openthinclient/otc-manager-home/"
otc_manager_install_path = "/opt/otc-manager/"


@pytest.mark.parametrize("service_name", [
    "openthinclient-manager",
])
def test_openthinclient_manager_service_running(host, service_name):
    time.sleep(20)
    service = host.service(service_name)
    assert service.is_running
    assert service.is_enabled


def test_openthinclient_manager_file(host):
    managerbin = host.file(otc_manager_install_path + "bin/openthinclient-manager")
    assert managerbin.user == "root"
    assert managerbin.group == "root"
    assert managerbin.exists is True


def test_openthinclient_install_directory(host):
    directory = host.file(otc_manager_install_path)
    assert directory.user == "root"
    assert directory.group == "root"
    assert directory.is_directory is True


def test_openthinclient_home_directory(host):
    directory = host.file("/home/openthinclient/otc-manager-home/")
    assert directory.user == "openthinclient"
    assert directory.group == "openthinclient"
    assert directory.is_directory is True


def test_openthinclient_legcacy_install_dir_symlink(host):
    directory = host.file("/opt/openthinclient")
    assert directory.user == "root"
    assert directory.group == "root"
    assert directory.is_symlink is True
    assert directory.linked_to == otc_manager_install_path.rstrip("/")


@pytest.mark.parametrize("executable,expected_output", [
    ('find /home/openthinclient/otc-manager-home/nfs/root/var/cache/archives/ -name "*.deb" -exec ls -A {} \;', ''),
])
def test_if_openthinclient_package_cache_dir_contains_deb_files(executable, expected_output, host):
    with host.sudo():
        cmd = host.run_test(executable)
        assert cmd.exit_status == 0
        assert cmd.stdout == expected_output


@pytest.mark.parametrize("filename", [
    (otc_manager_install_home + "nfs/root/sfs/base.sfs"),
    (otc_manager_install_home + "nfs/root/sfs/package/tcos-libs.sfs"),
    (otc_manager_install_home + "nfs/root/sfs/package/browser.sfs"),
    (otc_manager_install_home + "nfs/root/sfs/package/printserver.sfs"),
])
def test_if_otc_manager_default_install_packages_exists(host, filename):
    file = host.file(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists is True


@pytest.mark.parametrize("proto,port", [
    ("tcp", "10389"),
    ("tcp", "8080"),
])
def test_socket_openthinclient_manager_tcp_listening_ipv4_ipv6(host, proto, port):
    time.sleep(20)
    socketoptions = '{0}://{1}'.format(proto, port)
    socket = host.socket(socketoptions)
    assert socket.is_listening


@pytest.mark.parametrize("filename", [
    (otc_manager_install_home + ".appliance.properties"),
])
def test_otc_manager_appliance_properties_exists(host, filename):
    file = host.file(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists is True


@pytest.mark.parametrize("filename", [
    (otc_manager_install_home + ".installation.txt"),
])
def test_otc_manager_appliance_installation_flag_file_not_present(host, filename):
    file = host.file(filename)
    assert file.exists is False


@pytest.mark.parametrize("filename", [
    (otc_manager_install_home + "tftp.xml"),
    (otc_manager_install_home + "package-manager.xml"),
    (otc_manager_install_home + "directory/service.xml"),
    (otc_manager_install_home + "nfs/service.xml"),
])
def test_otc_manager_service_files_exists(host, filename):
    file = host.file(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists is True


@pytest.mark.parametrize("filename", [
    (otc_manager_install_home + "logs/"),
    (otc_manager_install_home + "nfs/"),
    (otc_manager_install_home + "nfs/home/"),
    (otc_manager_install_home + "nfs/root/"),
    (otc_manager_install_home + "nfs/root/custom"),
    (otc_manager_install_home + "nfs/root/sfs"),
])
def test_otc_manager_home_directories_permissions(host, filename):
    folder = host.file(filename)
    assert folder.user == "openthinclient"
    assert folder.group == "openthinclient"
    assert folder.exists is True


@pytest.mark.parametrize("filename,content", [
    (otc_manager_install_home + ".otc-manager-home.meta", "<server-id>"),
])
def test_otc_manager_metadata_file_for_server_id_present(host, filename, content):
    time.sleep(5)
    filen = host.file(filename)
    assert filen.exists is True
    assert filen.contains(content) is True


@pytest.mark.parametrize("filename,content", [
    (otc_manager_install_home + ".otc-manager-home.meta",
     "<acknowledged-privacy-notice-version>0</acknowledged-privacy-notice-version>"),
])
def test_otc_manager_metadata_file_for_privacy_notice_present(host, filename, content):
    filen = host.file(filename)
    assert filen.exists is True
    assert filen.contains(content) is True
