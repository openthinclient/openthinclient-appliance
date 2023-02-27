import pytest
import time

OTC_LDAP_BACKUP = "/usr/local/sbin/openthinclient-ldapbackup"
OTC_BACKUP_DIR = "/var/backups/openthinclient/"


class Test_OTC_Backup(object):

    @pytest.mark.parametrize("executable", [
        (OTC_LDAP_BACKUP),
    ])
    def test_openthinclient_backup(self, executable, host):
        with host.sudo():
            cmd = host.run_test(executable)
            assert cmd.exit_status == 0

    @pytest.mark.parametrize("executable,expected_output", [
        ("ls -A " + OTC_BACKUP_DIR, ""),
    ])
    def test_otc_backup_exists(self, executable, expected_output, host):
        time.sleep(2)
        with host.sudo():
            cmd = host.run_test(executable)
            assert cmd.exit_status == 0
            assert cmd.stdout != expected_output

    @pytest.mark.parametrize("content", [
        "Success",
    ])
    def test_otc_backup_success(self, host, content):
        files = host.file(OTC_BACKUP_DIR).listdir()
        for filename in files:
            filen = host.file(OTC_BACKUP_DIR + filename)
            assert filen.exists
            assert filen.contains(content)
            