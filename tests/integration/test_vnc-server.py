import pytest


@pytest.mark.parametrize("name,version", [
    ("x11vnc ", "0.9"),
    ("xvfb ", "2:1"),
    ("fluxbox ", "1.3"),
])
def test_vnc_packages_installed(host, name, version):
    pkg = host.package(name)
    assert pkg.is_installed
    assert pkg.version.startswith(version)


@pytest.mark.parametrize("service_name", [
    ("x11vnc"),
])
def test_service_running(host, service_name):
    service = host.service(service_name)
    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize("proto,hostname,port", [
    ("tcp", "0.0.0.0", "5900"),
])
def test_vnc_server_listening(host, proto, hostname, port):
    socketoptions = "{0}://{1}:{2}".format(proto, hostname, port)
    socket = host.socket(socketoptions)
    assert socket.is_listening


def test_x11vnc_service_file_present(host):
    managerbin = host.file("/etc/systemd/system/x11vnc.service")
    assert managerbin.user == "root"
    assert managerbin.group == "root"
    assert managerbin.exists is True


@pytest.mark.parametrize("filename", [
    "/home/openthinclient/.fluxbox/overlay",
    "/home/openthinclient/.fluxbox/lastwallpaper",
])
def test_fluxbox_settings_files_present(host, filename):
    file = host.file(filename)
    assert file.user == "openthinclient"
    assert file.group == "openthinclient"
    assert file.exists is True
