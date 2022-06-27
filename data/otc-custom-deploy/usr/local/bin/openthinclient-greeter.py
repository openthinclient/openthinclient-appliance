#!/usr/bin/env python3
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("LightDM", "1")

from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import LightDM
from time import strftime
import configparser
import datetime
import subprocess
import requests

UI_FILE_LOCATION = "/usr/local/share/openthinclient-greeter/openthinclient-greeter.ui"
CSS_FILE_LOCATION = "/usr/local/share/openthinclient-greeter/openthinclient-greeter.css"

translation = {
    "label_lang": ["Language:", "Sprache:"],
    "label_keyboard": ["Keyboard:", "Tastatur:"],
    "label_user": ["User:", "Benutzer:"],
    "password_label": ["Password:", "Passwort:"],
    "login_button": ["Login", "Einloggen"],
    "reboot_button": ["Reboot", "Neustarten"],
    "poweroff_button": ["Power Off", "Ausschalten"],
    "label_manager": ["openthinclient-Management server", "openthinclient-Management Server"],
    "manager_states": {
        "UP": "LÄUFT",
        "STARTING": "STARTET",
        "RESTARTING": "STARTET NEU",
        "UPDATING": "AKTUALISIERT",
        "INACTIVE": "INAKTIV"
    }
}

manager_state = None

clock = None
user_cb = None
greeter = None
login_clicked = None
password_entry = None
password_label = None
errorLabel = None
manager_label = None
manager_icon = None

lang_code = None
login_no = 0

layoutEntry = None
layout_cb = None
layoutStore = Gtk.ListStore(str)

builder = None

popupTime = None
intervalRunning = False

current_lang = "en"

cache_dir = "/var/lib/lightdm/.cache/openthinclient-greeter"
subprocess.run(f"mkdir -p {cache_dir}", shell=True)
state_file = "/var/lib/lightdm/.cache/openthinclient-greeter/state"
subprocess.run(f"touch {state_file}", shell=True)
cache = configparser.ConfigParser()
cache.read(str(state_file))


if not cache.has_section("greeter"):
    cache.add_section("greeter")

def write_cache():
    with open(str(state_file), 'w') as file:
        cache.write(file)

def set_language(lang="en"):
    index = 1 if lang == "de" else 0

    global current_lang
    current_lang = lang

    builder.get_object("label_lang").set_text(translation["label_lang"][index])
    builder.get_object("label_keyboard").set_text(translation["label_keyboard"][index])
    builder.get_object("label_user").set_text(translation["label_user"][index])
    builder.get_object("password_label").set_text(translation["password_label"][index])
    builder.get_object("label_manager").set_text(translation["label_manager"][index])
    builder.get_object("login_button").set_label(translation["login_button"][index])
    builder.get_object("reboot_button").set_label(translation["reboot_button"][index])
    builder.get_object("poweroff_button").set_label(translation["poweroff_button"][index])

    translate_manager_state()

def translate_manager_state():
    if manager_state is None: return

    if current_lang == "de":
        builder.get_object("manager_state_label").set_text(translation["manager_states"][manager_state])
    else:
        builder.get_object("manager_state_label").set_text(manager_state)


def update_clock():
    if clock == None: return False

    clock.set_text(strftime("%a, %d %b %H:%M:%S"))

    return True

def poweroff_click_handler(widget, data=None):
    if LightDM.get_can_shutdown():
        LightDM.shutdown()

def reboot_click_handler(widget, data=None):
    if LightDM.get_can_restart():
        LightDM.restart()

def fill_with_users(user_cb):
    user_id = 0
    last_user = cache.get("greeter", "last-user", fallback=None)

    for id, user in enumerate(LightDM.UserList().get_users()):
        user_cb.append_text(user.get_name())
        if user.get_name() == last_user:
            user_id = id

    user_cb.set_active(user_id)

def fill_with_layouts(layout_cb):
    layout_id = 0
    last_layout = cache.get("greeter", "last-layout", fallback="English (US)")

    layouts = []

    for id, layout in enumerate(LightDM.get_layouts()):
        layouts.append(layout.get_description())

    layouts.sort()
    for id, layout in enumerate(layouts):
        layoutStore.append([layout])
        if layout == last_layout:
            layout_id = id

    layout_cb.set_model(layoutStore)
    layout_cb.set_active(layout_id)

def fill_with_languages(lang_cb):
    lang_id = 0
    last_lang = cache.get("greeter", "last-lang", fallback="en_US.utf8")

    for id, lang in enumerate(LightDM.get_languages()):
        lang_cb.append_text(lang.get_name())
        if lang.get_code() == last_lang:
            lang_id = id

    lang_cb.set_active(lang_id)

def execute_layout_filter():
    layout_input = layoutEntry.get_text().upper()

    filteredStore = Gtk.ListStore(str)

    for layout in layoutStore:
        if not layout[0].upper().startswith(layout_input): continue

        filteredStore.append([layout[0]])

    layout_cb.set_model(filteredStore)

def layout_change_handler(widget, data=None):
    layout_obj = None

    for layout in LightDM.get_layouts():
        if layout.get_description().upper() == layoutEntry.get_text().upper():
            layout_obj = layout
            break

    if layout_obj is None:
        return

    cache.set("greeter", "last-layout", layout_obj.get_description())
    LightDM.set_layout(layout_obj)

def language_change_handler(widget, data=None):
    global lang_code
    lang_obj = None

    for lang in LightDM.get_languages():
        if lang.get_name() == lang_cb.get_active_text():
            lang_obj = lang
            break

    lang_code = lang_obj.get_code()
    cache.set("greeter", "last-lang", lang_code)

    if lang_code == "de_DE.utf8":
        set_language("de")
    elif lang_code == "en_US.utf8":
        set_language("en")

def user_change_handler(widget, data=None):
    global login_clicked
    login_clicked = False

    username = user_cb.get_active_text()
    cache.set("greeter", "last-user", username)

    if greeter.get_in_authentication():
        greeter.cancel_authentication()


    set_password_visibility(True)
    password_entry.set_text("")

    greeter.authenticate(username)

def login_click_handler(widget, data=None):
    global login_clicked
    login_clicked = True

    if greeter.get_is_authenticated():
        start_session()

    if greeter.get_in_authentication():
        greeter.cancel_authentication()

    username = user_cb.get_active_text()

    errorLabel.set_text("")
    greeter.authenticate(username)

def set_password_visibility(visible):
    password_entry.set_sensitive(visible)
    password_label.set_sensitive(visible)
    if visible:
        password_entry.show()
        password_label.show()
    else:
        password_entry.hide()
        password_label.hide()

def authentication_complete(greeter):
    if not login_clicked:
        set_password_visibility(False)

    else:
        if greeter.get_is_authenticated():
            start_session()
        else:
            display_error_message("Login failed")

def show_prompt(greeter, text, prompt_type=None, **kwargs):
    if login_clicked:
        greeter.respond(password_entry.get_text())
        password_entry.set_text("")

def start_session():
    if lang_code is not None:
        greeter.set_language(lang_code)

    write_cache()

    greeter.start_session_sync("")

def show_message(greeter, text, message_type=None, **kwargs):
    errorLabel.set_text(text)

def display_error_message(text, duration=5000):
    errorLabel.set_text("Login failed")

    global login_no
    login_no += 1
    local_login_no = login_no

    def inner():
        global login_no
        if local_login_no != login_no:
            return False

        errorLabel.set_text("")
        return False

    GLib.timeout_add(duration, inner)

def layout_entry_changed(widget, data=None):
    global intervalRunning
    global popupTime

    popupTime = datetime.datetime.now() + datetime.timedelta(milliseconds=750)

    if not intervalRunning:
        intervalRunning = True
        GLib.timeout_add(100, layout_entry_timeout_func)

def layout_entry_timeout_func():
    global popupTime

    if popupTime is None:
        return True

    if datetime.datetime.now() >= popupTime:
        execute_layout_filter()
        if len(layout_cb.get_model()) > 1:
            layout_cb.popup()
        popupTime = None

    return True

def set_manager_state():
    if manager_label is None: return False

    global manager_state

    try:
        resp = requests.get("http://localhost:8080/api/v2/server-status", allow_redirects=False)
        if resp.status_code == 302:
            state = "UP"
        else:
            state = resp.text
    except requests.exceptions.ConnectionError:
        state = "INACTIVE"
    finally:
        manager_label.set_text(state)
        manager_state = state

        if state == "UP":
            manager_icon.set_from_icon_name("gtk-yes", manager_icon.get_icon_name()[1])
        else:
            manager_icon.set_from_icon_name("gtk-no", manager_icon.get_icon_name()[1])

        translate_manager_state()
    return True

if __name__ == "__main__":
    builder = Gtk.Builder()
    greeter = LightDM.Greeter()
    greeter.connect("authentication-complete", authentication_complete)
    greeter.connect("show-prompt", show_prompt)
    greeter.connect("show-message", show_message)

    cursor = Gdk.Cursor(Gdk.CursorType.LEFT_PTR)
    builder.add_from_file(UI_FILE_LOCATION)

    set_language("en")

    cssProvider = Gtk.CssProvider()
    cssProvider.load_from_path(CSS_FILE_LOCATION)
    styleContext = Gtk.StyleContext()
    screen = Gdk.Screen.get_default()
    styleContext.add_provider_for_screen(screen, cssProvider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    poweroffButton = builder.get_object("poweroff_button")
    poweroffButton.connect("activate", poweroff_click_handler)

    rebootButton = builder.get_object("reboot_button")
    rebootButton.connect("activate", reboot_click_handler)

    password_entry = builder.get_object("password_entry")
    password_entry.connect("activate", login_click_handler)
    password_label = builder.get_object("password_label")

    errorLabel = builder.get_object("error_label")

    loginButton = builder.get_object("login_button")
    loginButton.connect("clicked", login_click_handler)

    user_cb = builder.get_object("user_cb")
    user_cb.connect("changed", user_change_handler)
    fill_with_users(user_cb)

    layout_cb = builder.get_object("layout_cb")
    layout_cb.connect("changed", layout_change_handler)
    layoutEntry = builder.get_object("layout_entry_field")
    fill_with_layouts(layout_cb)
    layoutEntry.connect("changed", layout_entry_changed)


    lang_cb = builder.get_object("language_cb")
    lang_cb.connect("changed", language_change_handler)
    fill_with_languages(lang_cb)

    ipLabel = builder.get_object("ip_label")

    ip = subprocess.run("hostname -I", capture_output=True, shell=True).stdout.decode().strip()
    ipLabel.set_text(f"IP: {ip}")

    manager_label = builder.get_object("manager_state_label")
    manager_icon = builder.get_object("manager_icon")
    set_manager_state()
    GLib.timeout_add(5000, set_manager_state)

    window = builder.get_object("window")

    greeter.connect_to_daemon_sync()

    clock = builder.get_object("clock")
    GLib.timeout_add(100, update_clock)

    window.get_root_window().set_cursor(cursor)

    screen = window.get_screen()
    window.resize(screen.get_width(), screen.get_height())

    if password_entry.get_sensitive():
        password_entry.grab_focus()
    else:
        user_cb.grab_focus()

    window.show()
    window.fullscreen()
    GLib.MainLoop().run()
