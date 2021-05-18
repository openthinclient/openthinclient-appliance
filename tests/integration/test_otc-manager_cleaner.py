import pytest
import time

otc_manager_install_path = "/opt/otc-manager/"
otc_cleaner_script = "/usr/local/sbin/openthinclient-cleaner"

OTC_INSTALL_HOME = "/home/openthinclient/otc-manager-home/"


class Test_OTC_Cleaner(object):

    @pytest.mark.parametrize("executable", [
        (otc_cleaner_script),
    ])
    def test_openthinclient_cleaner(self, executable, host):
        time.sleep(30)
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
        ("ls -A /var/lib/dhcp/", ""),
    ])
    def test_var_lib_dhcp_leases_files_deleted(self, executable, expected_output, host):
        with host.sudo():
            cmd = host.run_test(executable)
            assert cmd.exit_status == 0
            assert cmd.stdout == expected_output

    @pytest.mark.parametrize("filename", [
        "/root/.bash_history",
        "/home/openthinclient/.bash_history",
    ])
    def test_if_bash_history_files_are_deleted(self, host, filename):
        with host.sudo():
            file_name = host.file(filename)
            assert file_name.exists is False

    @pytest.mark.parametrize("filename", [
        "/var/log/apt/eipp.log.xz",
        "/var/log/lightdm/lightdm.log.old"
        "/var/log/lightdm/seat0-greeter.log.old",
        "/var/log/lightdm/x-0.log.old",
        "/var/log/Xorg.0.log.old",
    ])
    def test_if_var_log_files_are_deleted(self, host, filename):
        with host.sudo():
            logfile = host.file(filename)
            assert logfile.exists is False

    def test_udev_persistent_net_rules_exists(self, host):
        filen = host.file("/etc/udev/rules.d/70-persistent-net.rules")
        assert filen.exists is False

    @pytest.mark.parametrize("service_name", [
        "openthinclient-manager",
    ])
    def test_openthinclient_manager_service_not_running(self, host, service_name):
        time.sleep(30)
        service = host.service(service_name)
        assert service.is_running is False
        assert service.is_enabled

    @pytest.mark.parametrize("proto,port", [
        ("tcp", "10389"),
        ("tcp", "8080"),
    ])
    @pytest.mark.last
    def test_socket_openthinclient_manager_tcp_not_listening_ipv4_ipv6(self, host, proto, port):
        time.sleep(30)
        socketoptions = '{0}://{1}'.format(proto, port)
        socket = host.socket(socketoptions)
        assert socket.is_listening is False

    @pytest.mark.parametrize("filename,content", [
        (OTC_INSTALL_HOME + ".otc-manager-home.meta", "<server-id>"),
    ])
    def test_otc_manager_metadata_file_for_server_id_not_present(self, host, filename, content):
        time.sleep(30)
        filen = host.file(filename)
        assert filen.contains(content) is False
        assert filen.exists is True

    @pytest.mark.parametrize("filename,content", [
        (OTC_INSTALL_HOME + "directory/service.xml", "<accessControlEnabled>false</accessControlEnabled>"),
    ])
    def test_otc_manager_access_control_enabled_false(self, host, filename, content):
        time.sleep(30)
        filen = host.file(filename)
        assert filen.contains(content) is True
        assert filen.exists is True

