from pathlib import Path
import subprocess

from server import needs_data

CADDY_CONFIG_DIR = Path("/etc/caddy")


def reload_caddy():
    subprocess.run(['systemctl', 'reload', 'caddy'])


@needs_data
def set_https_status(server, data):
    try:
        symlink_target = ('Caddyfile_https' if data['enable_https']
                          else 'Caddyfile_http')

        (CADDY_CONFIG_DIR / 'Caddyfile').unlink(True)
        (CADDY_CONFIG_DIR / 'Caddyfile').symlink_to(
            CADDY_CONFIG_DIR / 'blocks' / symlink_target
        )
        reload_caddy()
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
