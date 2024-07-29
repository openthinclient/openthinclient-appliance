import gi

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")

from gi.repository import Gtk, WebKit2  # gir1.2-webkit2-3.0
from os.path import abspath, dirname, join

import signal
import sys
import os

CWD = abspath(dirname(__file__))
PID_FILE_PATH = "/var/run/user/1000/appliance-wizard-frontend.pid"

local_uri = 'http://localhost:4321'

class WebBrowser(object):
    def __init__(self):
        # Build GUI from Glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file(join(CWD, 'webbrowser.ui'))

        self.window = self.builder.get_object('window')

        if os.environ.get("LANG") == "de_DE.UTF-8":
            self.window.set_title("Erstkonfiguration")
        else:
            self.window.set_title("First start configuration")
        self.window.maximize()

        #self.window.connect("delete-event", lambda *_ : True)

        self.scrolled = self.builder.get_object('scrolled')

        self.webview = WebKit2.WebView()
        self.webview.connect('load-failed', Gtk.main_quit)
        self.webview.connect('load-changed', lambda _, e: handle_load_event(self.window, e))
        self.scrolled.add_with_viewport(self.webview)

        self.builder.connect_signals(self)
        self.window.connect('delete-event', Gtk.main_quit)

        self.webview.load_uri(local_uri)
        self.window.show_all()

def handle_load_event(window, event):
    # load successful
    if event == 3:
        window.show_all()

def handle_term(num, _):
    os.remove(PID_FILE_PATH)
    sys.exit(0)

if __name__ == '__main__':
    with open(PID_FILE_PATH, 'w') as f:
        f.write(str(os.getpid()))

    signal.signal(signal.SIGTERM, handle_term)

    gui = WebBrowser()
    Gtk.main()
