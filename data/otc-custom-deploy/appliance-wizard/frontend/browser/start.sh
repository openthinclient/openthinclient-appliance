#!/bin/bash

if [ -f /var/appliance-wizard/RUN.FLAG ]; then
  python3 /usr/local/share/appliance-wizard/frontend/browser/webbrowser.py
fi
