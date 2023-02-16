import subprocess

from server import needs_data


@needs_data
def timezone(server, data):
    try:
        cmd = f"sudo timedatectl set-timezone {data['timezone']}"
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
