#!/usr/bin/python3

import os
import subprocess


def _main():
    if not os.path.exists("/var/appliance-wizard/RUN.FLAG"):
        return

    subprocess.run(
        [
            "mount",
            "-o", "bind,ro",
            "/etc/lightdm/lightdm-firststart-override.conf",
            "/etc/lightdm/lightdm.conf"
        ]
    )

if __name__ == "__main__":
    _main()