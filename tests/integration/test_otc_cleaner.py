import pytest

otc_manager_install_path = "/opt/otc-manager/"
otc_cleaner_script = "/usr/local/sbin/openthinclient-cleaner"

OTC_INSTALL_HOME="/home/openthinclient/otc-manager-home/"

@pytest.mark.second_to_last
class Test_OTC_Cleaner(object):


    @pytest.mark.first
    @pytest.mark.parametrize("executable", [
        (otc_cleaner_script),
    ])

    @pytest.mark.first
    def test_openthinclient_cleaner(self, executable, host):
        with host.sudo():
            cmd = host.run_test(executable)
            assert cmd.exit_status == 0

    @pytest.mark.parametrize("service_name", [
        ("openthinclient-manager"),
    ])

    def test_openthinclient_manager_service_is_not_running(self, host, service_name):
        service = host.service(service_name)
        assert service.is_running is False

    @pytest.mark.parametrize("filename,content", [
        (OTC_INSTALL_HOME + ".otc-manager-home.meta", "<server-id>"),
    ])
    def test_otc_manager_metadata_file_for_server_id(host, filename, content):
        file = host.file(filename)
        assert file.contains(content) is False
        assert file.exists is True

    @pytest.mark.last
    def test_udev_persistent_net_rules_exists(self, host):
        file = host.file("/etc/udev/rules.d/70-persistent-net.rules")
        assert file.exists is False

