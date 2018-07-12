import pytest

otc_manager_install_path = "/opt/otc-manager/"


@pytest.mark.last
class Test_OTCManager_Uninstall(object):
    # def setup(self):
    # ssh_name = "openthinclient"
    # ssh_pass = "0pen%TC"
    # otc_manager_database_user = "openthinclient"
    # otc_manager_database_pass = "openthinclient"
    # otc_manager_default_pass = "0pen%TC"
    # otc_manager_install_home = "/home/openthinclient/otc-manager-home/"

    @pytest.mark.parametrize("executable", [
        (otc_manager_install_path + "support/uninstall -q"),
    ])
    @pytest.mark.first
    def test_openthinclient_uninstallation(self, executable, host):
        with host.sudo():
            cmd = host.run_test(executable)
            assert cmd.exit_status == 0

    @pytest.mark.parametrize("service_name", [
        ("openthinclient-manager"),
    ])
    def test_openthinclient_manager_service_is_not_running(self, host, service_name):
        service = host.service(service_name)
        assert service.is_running is False
        # assert service.is_enabled is False

    def test_openthinclient_manager_file_not_exists(self, host):
        managerbin = host.file(otc_manager_install_path + "/bin/openthinclient-manager")
        assert managerbin.exists is False

    @pytest.mark.parametrize("filename", [
        (otc_manager_install_path + "bin/openthinclient-manager"),
        (otc_manager_install_path + "bin/managerctl"),
        (otc_manager_install_path + "support/uninstall"),
        (otc_manager_install_path + "support/update-check"),
        ("/etc/init.d/openthinclient-manager"),
    ])
    def test_if_otc_manager_exuectable_files_exist(self, host, filename):
        filen = host.file(filename)
        assert filen.exists is False

    @pytest.mark.parametrize("directory", [
        (otc_manager_install_path + ".install4j/"),
        (otc_manager_install_path + "support/"),
        (otc_manager_install_path + "lib/"),
    ])
    def test_openthinclient_install_subdirectory_after_uninstall(self, host, directory):
        directory = host.file(directory)
        assert directory.is_directory is False

    @pytest.mark.last
    def test_openthinclient_install_directory_after_uninstall(self, host):
        directory = host.file(otc_manager_install_path)
        assert directory.user == "root"
        assert directory.group == "root"
        assert directory.is_directory is False
