import pytest
import re

# set some default variables

ssh_name = "openthinclient"
ssh_pass = "0pen%TC"
otc_manager_database_user = "openthinclient"
otc_manager_database_pass = "openthinclient"

otc_manager_default_pass = "0pen%TC"
otc_manager_install_home = "/home/openthinclient/otc-manager-home/"


@pytest.mark.first
@pytest.mark.parametrize("executable", [
    ("/opt/openthinclient/support/uninstall -q"),
])

@pytest.mark.first
def test_openthinclient_uninstallation(executable, host):
    with host.sudo():
        cmd = host.run_test(executable)
        assert cmd.exit_status == 0

@pytest.mark.parametrize("service_name", [
    ("openthinclient-manager"),
])

def test_openthinclient_manager_service_is_not_running(host, service_name):
    service = host.service(service_name)
    assert service.is_running is False
    # assert service.is_enabled is False

def test_openthinclient_manager_file_not_exists(host):
    managerbin = host.file("/opt/openthinclient/bin/openthinclient-manager")
    assert managerbin.exists is False

@pytest.mark.parametrize("filename", [
    ("/opt/openthinclient/bin/openthinclient-manager"),
    ("/opt/openthinclient/bin/managerctl"),
    ("/opt/openthinclient/support/uninstall"),
    ("/opt/openthinclient/support/update-check"),
    ("/etc/init.d/openthinclient-manager"),
])

def test_if_otc_manager_exuectable_files_exist(host, filename):
    file = host.file(filename)
    assert file.exists is False


@pytest.mark.parametrize("directory", [
    ("/opt/openthinclient/.install4j/"),
    ("/opt/openthinclient/support/"),
    ("/opt/openthinclient/lib/"),
])

def test_openthinclient_install_subdirectory_after_uninstall(host, directory):
    directory = host.file(directory)
    assert directory.is_directory is False


@pytest.mark.last
def test_openthinclient_install_directory_after_uninstall(host):
    directory = host.file("/opt/openthinclient/")
    assert directory.user == "root"
    assert directory.group == "root"
    assert directory.is_directory is True
