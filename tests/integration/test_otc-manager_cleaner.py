import pytest
import time

otc_manager_install_path = "/opt/otc-manager/"
otc_cleaner_script = "/usr/local/sbin/openthinclient-cleaner"

OTC_INSTALL_HOME = "/home/openthinclient/otc-manager-home/"


@pytest.mark.second_to_last
class Test_OTC_Cleaner(object):

    @pytest.mark.parametrize("executable", [
        (otc_cleaner_script),
    ])
    @pytest.mark.first
    def test_openthinclient_cleaner(self, executable, host):
        with host.sudo():
            cmd = host.run_test(executable)
            assert cmd.exit_status == 0

    @pytest.mark.parametrize("executable,expected_output", [
        ("ls -A " + OTC_INSTALL_HOME + "logs/", ""),
    ])
    def test_otc_manager_home_log_dir_empty(self, executable, expected_output, host):
        with host.sudo():
            cmd = host.run_test(executable)
            assert cmd.exit_status == 0
            assert cmd.stdout == expected_output

    @pytest.mark.parametrize("executable,expected_output", [
        ("ls -A " + OTC_INSTALL_HOME + "nfs/home/", ""),
    ])
    def test_otc_manager_home_nfs_home_dir_empty(self, executable, expected_output, host):
        with host.sudo():
            cmd = host.run_test(executable)
            assert cmd.exit_status == 0
            assert cmd.stdout == expected_output

    @pytest.mark.parametrize("executable,expected_output", [
        ("ls -A /var/cache/oracle-jdk8-installer/", ""),
    ])
    def test_oracle_java_cache_dir_emtpy(self, executable, expected_output, host):
        with host.sudo():
            cmd = host.run_test(executable)
            assert cmd.exit_status == 0
            assert cmd.stdout == expected_output

    @pytest.mark.parametrize("executable,expected_output", [
        ("ls -A /var/lib/dhcp/", ""),
    ])
    def test_var_lib_dhcp_leases_files_deleted(self, executable, expected_output, host):
        with host.sudo():
            cmd = host.run_test(executable)
            assert cmd.exit_status == 0
            assert cmd.stdout == expected_output

    # @pytest.mark.parametrize("executable,expected_output", [
    #     ("ls -A /tmp", ""),
    # ])
    # def test_tmp_folder_empty(self, executable, expected_output, host):
    #     with host.sudo():
    #         cmd = host.run_test(executable)
    #         assert cmd.exit_status == 0
    #         assert cmd.stdout == expected_output

    @pytest.mark.parametrize("filename", [
        ("/root/.bash_history"),
        ("/home/openthinclient/.bash_history"),
    ])
    def test_if_bash_history_files_are_deleted(self, host, filename):
        with host.sudo():
            file = host.file(filename)
            assert file.exists is False

    # @pytest.mark.parametrize("executable,expected_output", [
    #     ("ls -A /var/log/", ""),
    # ])
    # def test_var_log_directory_is_empty(self, executable, expected_output, host):
    #     with host.sudo():
    #         cmd = host.run_test(executable)
    #         assert cmd.exit_status == 0
    #         assert cmd.stdout == expected_output

    def test_udev_persistent_net_rules_exists(self, host):
        filen = host.file("/etc/udev/rules.d/70-persistent-net.rules")
        assert filen.exists is False

    # @pytest.mark.parametrize("service_name", [
    #    ("openthinclient-manager.service"),
    # ])
    # def test_openthinclient_manager_service_is_not_running(self, host, service_name):
    #     with host.sudo():
    #         service = host.service(service_name)
    #         assert service.is_running is False
    #         assert service.is_enabled is True

    @pytest.mark.parametrize("proto,port", [
        ("tcp", "10389"),
        ("tcp", "8080"),
    ])
    @pytest.mark.last
    def test_socket_openthinclient_manager_tcp_not_listening_ipv4_ipv6(self, host, proto, port):
        time.sleep(15)
        socketoptions = '{0}://{1}'.format(proto, port)
        socket = host.socket(socketoptions)
        assert socket.is_listening is False

    @pytest.mark.parametrize("filename,content", [
        (OTC_INSTALL_HOME + ".otc-manager-home.meta", "<server-id>"),
    ])
    @pytest.mark.second_to_last
    def test_otc_manager_metadata_file_for_server_id(self, host, filename, content):
        time.sleep(20)
        filen = host.file(filename)
        assert filen.contains(content) is False
        assert filen.exists is True
