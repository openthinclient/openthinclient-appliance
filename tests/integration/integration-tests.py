import pytest

@pytest.mark.parametrize("name,version", [
    ("mysql-server", "5.5"),
    ("python", "2.7"),
])
def test_packages(Package, name, version):
    assert Package(name).is_installed
    assert Package(name).version.startswith(version)


@pytest.mark.parametrize("user", [
    ("root"),
    ("openthinclient"),
])

def test_user_in_passwd_file(File, user):
    passwd = File("/etc/passwd")
    assert passwd.contains(user)


@pytest.mark.parametrize("service_name", [
    ("openthinclient-manager"),
    ("lightdm"),
    ("mysql"),
])

def test_service_running(Service, service_name):
    service = Service(service_name)
    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize("proto,host,port", [
    ("tcp", "127.0.0.1", "3306"),
    ("tcp", "0.0.0.0","22"),
])

def test_socket_listening(Socket, proto, host, port):
    socketoptions = "{0}://{1}:{2}".format(proto, host, port)
    socket = Socket(socketoptions)
    assert socket.is_listening


def test_passwd_file(File):
    passwd = File("/etc/passwd")
    assert passwd.contains("root")
    assert passwd.user == "root"
    assert passwd.group == "root"
    assert passwd.mode == 0o644

def test_openthinclient_manager_file(File):
    managerbin = File("/opt/openthinclient/bin/openthinclient-manager")
    assert managerbin.user == "root"
    assert managerbin.group == "root"
    assert managerbin.exists == True

