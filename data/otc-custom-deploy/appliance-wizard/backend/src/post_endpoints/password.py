import subprocess
from xml.etree import ElementTree
import ldap3
import time

from server import needs_data

LDAP_SERVICE_FILE = "/home/openthinclient/otc-manager-home/directory/service.xml"
LDAP_SERVER = ("localhost", 10389)

def _get_ldap_credentials():
    tree = ElementTree.parse(LDAP_SERVICE_FILE)
    root = tree.getroot()

    user = root.find("contextProviderURL").text
    password = root.find("contextSecurityCredentials").text

    return user, password

LDAP_ADMINISTRATOR_USER_DN = "cn=administrator,ou=users,ou=openthinclient,dc=openthinclient,dc=org"

@needs_data
def password(server, data):
    try:
        cmd = f"echo openthinclient:{data['password']} | sudo chpasswd"
        process = subprocess.run(cmd, shell=True).check_returncode()
    except subprocess.CalledProcessError:
        server.respond(
            500,
            {"Content-Type": "application/json"},
            {"successful": False}
        )
        return
    except KeyError:
        server.respond(
            400,
            {"Content-Type": "application/json"},
            {"successful": False}
        )
        return

    server.respond(
        200,
        {"Content-Type": "application/json"},
        {"successful": True}
    )

@needs_data
def password_management(server, data):
    try:
        c = _connect_to_ldap()
        if c == None:
            server.respond(500, {"Content-Type": "application/json"}, {"successful": False})
            return

        res = c.modify(LDAP_ADMINISTRATOR_USER_DN, {'userPassword': [(ldap3.MODIFY_REPLACE, [data['password']])]})
        if res == False:
            server.respond(500, {"Content-Type": "application/json"}, {"successful": False})
            return

        c.unbind()
    except:
        server.respond(500, {"Content-Type": "application/json"}, {"successful": False})
        return

    server.respond(200, {"Content-Type": "application/json"}, {"successful": True})


def _connect_to_ldap():
    for i in range(100):
        try:
            s = ldap3.Server(*LDAP_SERVER)
            c = ldap3.Connection(s, *_get_ldap_credentials())
            c.bind()
            return c
        except:
            pass

        time.sleep(2)
