import pytest
import re

# set some default variables

ssh_name = "openthinclient"
ssh_pass = "0pen%TC"
otc_manager_database_user = "openthinclient"
otc_manager_database_pass = "openthinclient"

otc_manager_default_pass = "0pen%TC"
otc_manager_install_home = "/home/openthinclient/otc-manager-home/"
otc_manager_install_path = "/opt/otc-manager/"


@pytest.mark.parametrize("service_name", [
    ("openthinclient-manager"),
])

def test_openthinclient_manager_service_running(host, service_name):
    service = host.service(service_name)
    assert service.is_running
    assert service.is_enabled


def test_openthinclient_manager_file(host):
    managerbin = host.file(otc_manager_install_path + "/bin/openthinclient-manager")
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
    assert directory.user == "root"
    assert directory.group == "root"
    assert directory.is_directory is True


@pytest.mark.parametrize("executable,expected_output", [
    ("mysql -uroot -proot -e 'use openthinclient;'", ""),
])
def test_if_openthinclient_mysql_db_exists(executable, expected_output, host):
    with host.sudo():
        cmd = host.run_test(executable)
        assert cmd.exit_status == 0
        assert cmd.stderr == expected_output


@pytest.mark.parametrize("executable,expected_output", [
    ("mysql -uroot -proot -sse 'SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = \"openthinclient\")';", "1\n"),
])
def test_if_openthinclient_mysql_user_exists(executable, expected_output, host):
    with host.sudo():
        cmd = host.run_test(executable)
        assert cmd.exit_status == 0
        assert cmd.stdout == expected_output


@pytest.mark.parametrize("executable,expected_output", [
    ("mysql -u" + otc_manager_database_user + " -p" + otc_manager_database_user + " -e 'use openthinclient;'", ""),
])
def test_if_openthinclient_user_has_access_to_mysql_db(executable, expected_output, host):
    with host.sudo():
        cmd = host.run_test(executable)
        assert cmd.exit_status == 0
        assert cmd.stderr == expected_output


@pytest.mark.parametrize("executable,expected_output", [
    ("ls -A /home/openthinclient/otc-manager-home/nfs/root/var/cache/archives/1/", ""),
])
def test_if_openthinclient_package_cache_dir_is_empty(executable, expected_output, host):
    with host.sudo():
        cmd = host.run_test(executable)
        assert cmd.exit_status == 0
        assert cmd.stdout == expected_output


@pytest.mark.parametrize("filename", [
    (otc_manager_install_home + "nfs/root/sfs/base.sfs"),
    (otc_manager_install_home + "nfs/root/sfs/package/tcos-scripts.sfs"),
    (otc_manager_install_home + "nfs/root/sfs/package/tcos-libs.sfs"),
])

def test_if_otc_manager_default_install_packages_exists(host, filename):
    file = host.file(filename)
    assert file.user == "root"
    assert file.group == "root"
    assert file.exists is True


@pytest.mark.parametrize("filename,content", [
    (otc_manager_install_home + "db.xml", "jdbc:mysql://localhost:3306/openthinclient"),
])

def test_otc_manager_db_xml_settings(host, filename, content):
    file = host.file(filename)
    assert file.contains(content)
    assert file.exists is True