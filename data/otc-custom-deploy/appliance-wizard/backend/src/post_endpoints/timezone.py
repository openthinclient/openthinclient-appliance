import subprocess

from server import needs_data


@needs_data
def timezone(server, data):
    try:
        subprocess.run(
            ('sudo', 'timedatectl', 'set-timezone', f'{data["timezone"]}')
        ).check_returncode()
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
