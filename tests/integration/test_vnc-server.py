import pytest


@pytest.mark.parametrize("name,version", [
    ("x11vnc ", "0.9"),
    ("xvfb ", "2:1"),
    ("fluxbox ", "1.3"),
    ("openbox", "3.6")
])
def test_vnc_packages_installed(host, name, version):
    pkg = host.package(name)
    assert pkg.is_installed
    assert pkg.version.startswith(version)


@pytest.mark.parametrize("service_name", [
    ("x11vnc"),
    ("xvfb"),
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
    filename = host.file("/etc/systemd/system/x11vnc.service")
    assert filename.user == "root"
    assert filename.group == "root"
    assert filename.exists is True


def test_xvfb_service_file_present(host):
    filename = host.file("/etc/systemd/system/xvfb.service")
    assert filename.user == "root"
    assert filename.group == "root"
    assert filename.exists is True


@pytest.mark.parametrize("filename", [
    ("/usr/local/bin/openthinclient-vnc-starter"),
    ("/usr/local/bin/openthinclient-vnc-xvfb"),
])
def test_otc_usr_local_bin_vnc_starter(host, filename):
    filen = host.file(filename)
    assert filen.user == "openthinclient"
    assert filen.group == "openthinclient"
    assert filen.exists is True


@pytest.mark.parametrize("filename", [
    "/home/openthinclient/.config/openbox/rc.xml",
])
def test_openbox_settings_files_present(host, filename):
    filen = host.file(filename)
    assert filen.user == "openthinclient"
    assert filen.group == "openthinclient"
    assert filen.exists is True


@pytest.mark.parametrize("filename", [
    "/home/openthinclient/.fluxbox/overlay",
    "/home/openthinclient/.fluxbox/lastwallpaper",
    "/home/openthinclient/.fluxbox/startup",
])
def test_fluxbox_settings_files_present(host, filename):
    filen = host.file(filename)
    assert filen.user == "openthinclient"
    assert filen.group == "openthinclient"
    assert filen.exists is True


@pytest.mark.parametrize("filename,expected_output", [
    ("/home/openthinclient/.fluxbox/overlay",
     "background: aspect \n"
     "background.pixmap: /usr/local/share/openthinclient/backgrounds/openthinclient-server-Desktop-Pales.jpg"),
])
def test_fluxbox_overlay_file_settings(filename, expected_output, host):
        filen = host.file(filename)
        assert filen.contains(expected_output)


@pytest.mark.parametrize("filename,expected_output", [
    ("/home/openthinclient/.fluxbox/startup",
     "/usr/local/bin/openthinclient-manager &"),
])
def test_fluxbox_startup_file_contents(filename, expected_output, host):
        filen = host.file(filename)
        assert filen.contains(expected_output)


@pytest.mark.parametrize("filename,content", [
    ("/usr/bin/x11vnc --version", "x11vnc: 0.9.15 lastmod: 2018-02-04"),
])
def test_x11_vnc_version(host, filename, content):
    with host.sudo():
        test = host.check_output(filename)
        assert test == content


@pytest.mark.parametrize("filename", [
    "/usr/bin/x11vnc",
])
def test_x11_vnc_permissions(host, filename):
    filen = host.file(filename)
    assert filen.user == "root"
    assert filen.group == "staff"
    assert filen.exists is True
