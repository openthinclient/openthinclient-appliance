import subprocess

from server import needs_data

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
