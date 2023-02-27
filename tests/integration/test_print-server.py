import pytest

@pytest.mark.parametrize("name", [
    ("cups"),
    ("cups-client"),
    ("cups-bsd"),
    ("cups-browsed"),
    ('printer-driver-cups-pdf'),
    ("printer-driver-hpijs"),
])
def test_packages_installed(host, name):
    pkg = host.package(name)
    assert pkg.is_installed


@pytest.mark.parametrize("proto,hostname,port", [
    ("tcp", "127.0.0.1", "631"),
    ("tcp", "0.0.0.0","631"),
])
def test_cups_listening(host, proto, hostname, port):
    socketoptions = "{0}://{1}:{2}".format(proto, hostname, port)
    socket = host.socket(socketoptions)
    assert socket.is_listening


@pytest.mark.parametrize("service_name", [
    ("cups"),
])
def test_service_running(host, service_name):
    service = host.service(service_name)
    assert service.is_enabled
    assert service.is_running


@pytest.mark.parametrize("filename,content", [
    ("/etc/cups/cupsd.conf","# Allow remote access to the configuration files..."),
    ("/etc/cups/cupsd.conf","# Allow remote administration..."),
])
def test_cupsd_config_content(host, filename, content):
    with host.sudo():
        filen = host.file(filename)
        assert filen.exists
        assert filen.contains(content)
        assert filen.user == "root"
        assert filen.group == "lp"
