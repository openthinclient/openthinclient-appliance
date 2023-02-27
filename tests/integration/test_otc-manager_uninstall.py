import pytest

otc_manager_install_path = "/opt/otc-manager/"


class Test_OTCManager_Uninstall(object):

    @pytest.mark.parametrize("executable", [
        (otc_manager_install_path + "uninstall -q"),
    ])
    def test_openthinclient_uninstallation(self, executable, host):
        with host.sudo():
            cmd = host.run_test(executable)
            assert cmd.exit_status == 0

    @pytest.mark.parametrize("service_name", [
        ("openthinclient-manager"),
    ])
    def test_openthinclient_manager_service_is_not_running(self, host, service_name):
        service = host.service(service_name)
        assert not service.is_running

    def test_openthinclient_manager_file_not_exists(self, host):
        managerbin = host.file(otc_manager_install_path + "/bin/openthinclient-manager")
        assert not managerbin.exists

    @pytest.mark.parametrize("filename", [
        (otc_manager_install_path + "bin/openthinclient-manager"),
        (otc_manager_install_path + "bin/managerctl"),
        (otc_manager_install_path + "support/uninstall"),
        (otc_manager_install_path + "support/update-check"),
        "/etc/init.d/openthinclient-manager",
    ])
    def test_if_otc_manager_exuectable_files_exist(self, host, filename):
        filen = host.file(filename)
        assert not filen.exists

    @pytest.mark.parametrize("directory", [
        (otc_manager_install_path + ".install4j/"),
        (otc_manager_install_path + "support/"),
        (otc_manager_install_path + "lib/"),
    ])
    def test_openthinclient_install_subdirectory_after_uninstall(self, host, directory):
        directory = host.file(directory)
        assert not directory.is_directory

    def test_openthinclient_install_directory_after_uninstall(self, host):
        dir_content = host.run("ls -ld $(find " + otc_manager_install_path + " )")
        print("Contents of: " + otc_manager_install_path)
        print(dir_content.stdout)

        directory = host.file(otc_manager_install_path)
        assert not directory.is_directory
