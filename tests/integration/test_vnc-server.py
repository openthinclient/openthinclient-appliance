import pytest


@pytest.mark.parametrize("name,version", [
    ("x11vnc", "0.9"),
    ("xvfb", "2:1"),
    ("openbox", "3.6"),
    ("python-pip", "9.0"),
    ("python-wheel", "0.29")
])
def test_vnc_packages_installed(host, name, version):
    pkg = host.package(name)
    assert pkg.is_installed
    assert pkg.version.startswith(version)


@pytest.mark.parametrize("service_name", [
    "x11vnc",
    "xvfb",
    "websockify"
])
def test_service_running(host, service_name):
    service = host.service(service_name)
    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize("proto,hostname,port", [
    ("tcp", "0.0.0.0", "5900"),
    ("tcp", "127.0.0.1", "5910"),
])
def test_vnc_server_listening(host, proto, hostname, port):
    socket_options = "{0}://{1}:{2}".format(proto, hostname, port)
    socket = host.socket(socket_options)
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


def test_websockify_service_file_present(host):
    filename = host.file("/etc/systemd/system/websockify.service")
    assert filename.user == "root"
    assert filename.group == "root"
    assert filename.exists is True


def test_websockify_binary_file_present(host):
    filename = host.file("/usr/local/bin/websockify")
    assert filename.user == "root"
    assert filename.group == "staff"
    assert filename.exists is True


@pytest.mark.parametrize("filename", [
    "/usr/local/share/websockify/include/",
    "/usr/local/lib/python2.7/dist-packages/websockify/",
])
def test_websockify_python_package_deps(host, filename):
    filen = host.file(filename)
    assert filen.user == "root"
    assert filen.group == "staff"
    assert filen.exists is True


@pytest.mark.parametrize("filename", [
    "/usr/local/bin/openthinclient-vnc-starter",
    "/usr/local/bin/openthinclient-vnc-xvfb",
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
