import subprocess

from server import needs_data
from constants import *

def do_manual_proxy_configuration(proxy_type, server, data):
    try:
        if data.get('reset', False) == True:
            for key in data["keys"]:
                cmd = "sudo -u openthinclient DBUS_SESSION_BUS_ADDRESS="\
                    "\"unix:path=/run/user/1000/bus\" "\
                    f"gsettings reset org.gnome.system.proxy.{proxy_type} {key}"
                process = subprocess.run(cmd, shell=True).check_returncode()
        else:
            for key in data.keys():
                if proxy_type == "http":
                    option_keys = PROXY_HTTP_OPTION_KEYS
                elif proxy_type == "https":
                    option_keys = PROXY_HTTPS_OPTION_KEYS
                elif proxy_type == "ftp":
                    option_keys = PROXY_FTP_OPTION_KEYS
                elif proxy_type == "socks":
                    option_keys = PROXY_SOCKS_OPTION_KEYS

                if key not in option_keys:
                    continue

                cmd = "sudo -u openthinclient DBUS_SESSION_BUS_ADDRESS="\
                    "\"unix:path=/run/user/1000/bus\" gsettings set "\
                    f"org.gnome.system.proxy.{proxy_type} {key} {data[key]}"
                process = subprocess.run(cmd, shell=True).check_returncode()
    except subprocess.CalledProcessError:
        server.respond(
            500,
            {"Content-Type": "application/json"},
            {"successfull": False}
        )
        return
    except KeyError:
        server.respond(
            400,
            {"Content-Type": "application/json"},
            {"successfull": False})
        return

    server.respond(
        200,
        {"Content-Type": "application/json"},
        {"successfull": True}
    )


@needs_data
def mode(server, data):
    try:
        if data.get("reset", False) == True:
            cmd = "sudo -u openthinclient DBUS_SESSION_BUS_ADDRESS="\
                "\"unix:path=/run/user/1000/bus\" gsettings reset "\
                "org.gnome.system.proxy mode"
        else:
            cmd = f"sudo -u openthinclient DBUS_SESSION_BUS_ADDRESS="\
                "\"unix:path=/run/user/1000/bus\" gsettings set "\
                f"org.gnome.system.proxy mode {data['mode']}"
        process = subprocess.run(cmd, shell=True).check_returncode()
    except subprocess.CalledProcessError:
        server.respond(
            500,
            {"Content-Type": "application/json"},
            {"successfull": False}
        )
        return
    except KeyError:
        server.respond(
            400,
            {"Content-Type": "application/json"},
            {"successfull": False}
        )
        return

    server.respond(
        200,
        {"Content-Type": "application/json"},
        {"successfull": True}
    )


@needs_data
def autoconfig_url(server, data):
    try:
        if data.get("reset", False) == True:
            cmd = "sudo -u openthinclient DBUS_SESSION_BUS_ADDRESS="\
                "\"unix:path=/run/user/1000/bus\" gsettings reset "\
                "org.gnome.system.proxy autoconfig-url"
        else:
            cmd = f"sudo -u openthinclient DBUS_SESSION_BUS_ADDRESS="\
                "\"unix:path=/run/user/1000/bus\" gsettings set "\
                f"org.gnome.system.proxy autoconfig-url {data['autoconfig']}"
        process = subprocess.run(cmd, shell=True).check_returncode()
    except subprocess.CalledProcessError:
        server.respond(
            500,
            {"Content-Type": "application/json"},
            {"successfull": False}
        )
        return
    except KeyError:
        server.respond(
            400,
            {"Content-Type": "application/json"},
            {"successfull": False}
        )
        return

    server.respond(
        200,
        {"Content-Type": "application/json"},
        {"successfull": True}
    )


@needs_data
def ignored(server, data):
    try:
        if data.get("reset", False) == True:
            cmd = "sudo -u openthinclient DBUS_SESSION_BUS_ADDRESS="\
                "\"unix:path=/run/user/1000/bus\" gsettings reset "\
                "org.gnome.system.proxy ignore-hosts"
        else:
            hosts = str(data['hosts']).replace("'", '"')
            cmd = f"sudo -u openthinclient DBUS_SESSION_BUS_ADDRESS="\
                "\"unix:path=/run/user/1000/bus\" gsettings set "\
                f"org.gnome.system.proxy ignore-hosts '{hosts}'"
        process = subprocess.run(cmd, shell=True).check_returncode()
    except subprocess.CalledProcessError:
        server.respond(
            500,
            {"Content-Type": "application/json"},
            {"successfull": False}
        )
        return
    except KeyError:
        server.respond(
            400,
            {"Content-Type": "application/json"},
            {"successfull": False}
        )
        return

    server.respond(
        200,
        {"Content-Type": "application/json"},
        {"successfull": True}
    )


@needs_data
def http(server, data):
    do_manual_proxy_configuration("http", server, data)


@needs_data
def https(server, data):
    do_manual_proxy_configuration("https", server, data)


@needs_data
def ftp(server, data):
    do_manual_proxy_configuration("ftp", server, data)


@needs_data
def socks(server, data):
    do_manual_proxy_configuration("socks", server, data)
