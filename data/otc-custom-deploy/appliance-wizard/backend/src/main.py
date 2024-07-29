from http.server import HTTPServer
import os
import subprocess
import sys

from server import WizardServer
from post_endpoints.password import password
from post_endpoints.proxy import (
    mode,
    autoconfig_url,
    ignored,
    http,
    https,
    ftp,
    socks
)
from post_endpoints.timezone import timezone

from constants import *

@WizardServer.endpoint("api/v1/term_frontend")
def term_frontend(server):
    try:
        if not os.path.exists("/var/run/user/1000/appliance-wizard-frontend.pid"):
            server.respond(
                204,
                {},
                {}
            )
            return
        with open(PID_FILE_PATH, 'r') as f:
            pid = f.read().strip()
        cmd = f"kill -15 {pid}"
        process = subprocess.run(cmd, shell=True)
    except Exception as e:
        server.respond(
            500,
            {"Content-Type": "application/json"},
            {"successful": False}
        )
        return

    server.respond(
        200,
        {"Content-Type": "application/json"},
        {"successful": True}
    )

    sys.exit(0)


@WizardServer.endpoint("api/v1/deactivate")
def destroy(server):
    try:
        os.remove("/var/appliance-wizard/RUN.FLAG")
    except:
        server.respond(
            500,
            {"Content-Type": "application/json"},
            {"successful": False}
        )

    server.respond(
        200,
        {"Content-Type": "application/json"},
        {"successful": True}
    )


@WizardServer.endpoint("api/v1/timezones")
def timezones(server):
    try:
        cmd = "timedatectl list-timezones"
        process = subprocess.run(cmd, shell=True, capture_output=True)
        timezones = process.stdout.decode().strip().split('\n')
    except:
        server.respond(
            500,
            {"Content-Type": "application/json"},
            {"successful": False}
        )

    server.respond(
        200,
        {"Content-Type": "application/json"},
        {"timezones": timezones}
    )


@WizardServer.endpoint("")
def index(server):
    res = get_resource("assets/index.html")

    server.send_response(200)
    server.end_headers()
    for i in res:
        server.wfile.write(i)


@WizardServer.endpoint("*")
def resource(server):
    if server.path == "/":
        server.not_found()
        return

    path = f"assets/{server.path.split('/', 1)[-1]}"

    if not os.path.exists(path):
        server.not_found()
        return

    res = get_resource(path)

    server.send_response(200)

    file_end = server.path.split('/', 1)[-1].split('.')[-1]
    if file_end == 'scss':
        server.send_header("Content-Type", "text/scss")
    if file_end == 'js':
        server.send_header("Content-Type", "application/javascript")
    if file_end == 'json':
        server.send_header("Content-Type", "application/json")

    server.end_headers()
    for i in res:
        server.wfile.write(i)


def get_resource(path):
    if not os.path.exists(path):
        return None

    try:
        with open(path, 'rb') as f:
            data = f.read(BUFFER_SIZE)
            while data:
                yield data
                data = f.read(BUFFER_SIZE)

    except:
        return None

def setup_post_endpoints():
    WizardServer.endpoint("api/v1/password", methods=["POST"])(password)

    WizardServer.endpoint("api/v1/proxy/mode", methods=["POST"])(mode)
    WizardServer.endpoint("api/v1/proxy/autoconfig", methods=["POST"])(autoconfig_url)
    WizardServer.endpoint("api/v1/proxy/ignored", methods=["POST"])(ignored)
    WizardServer.endpoint("api/v1/proxy/manual/http", methods=["POST"])(http)
    WizardServer.endpoint("api/v1/proxy/manual/https", methods=["POST"])(https)
    WizardServer.endpoint("api/v1/proxy/manual/ftp", methods=["POST"])(ftp)
    WizardServer.endpoint("api/v1/proxy/manual/socks", methods=["POST"])(socks)

    WizardServer.endpoint("api/v1/timezone", methods=["POST"])(timezone)


if __name__ == "__main__":
    print(f"Server running at http://{HOST}:{PORT}")
    print(f"User id: {os.getuid()}")
    
    setup_post_endpoints()

    try:
        web_server = HTTPServer((HOST, PORT), WizardServer)
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
