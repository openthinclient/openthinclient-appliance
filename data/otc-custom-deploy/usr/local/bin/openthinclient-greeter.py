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
import subprocess
import requests

settings = Gtk.Settings.get_default()
settings.set_property("gtk-icon-theme-name", "ContrastHigh")

SERVER_STATUS_URL = "http://localhost:8080/api/v2/server-status"

UI_FILE_LOCATION = "/usr/local/share/openthinclient-greeter/openthinclient-greeter.ui"
UI_LAYOUT_CHOOSER_FILE_LOCATION = "/usr/local/share/openthinclient-greeter/openthinclient-greeter2.ui"
CSS_FILE_LOCATION = "/usr/local/share/openthinclient-greeter/openthinclient-greeter.css"

translation = {
    "label_lang": ["Language / Sprache", "Sprache / Language"],
    "label_keyboard": ["Keyboard", "Tastatur"],
    "label_user": ["User:", "Benutzer:"],
    "password_label": ["Password:", "Passwort:"],
    "login_button": ["Login", "Einloggen"],
    "reboot_button": ["Reboot", "Neustarten"],
    "poweroff_button": ["Power Off", "Ausschalten"],
    "label_manager": [
        "openthinclient-Management server",
        "openthinclient-Management Server"
    ],
    'status.login': ['Logging in', 'Anmeldung wird durchgeführt'],
    'status.login_failed': ['Login failed', 'Anmeldung gescheitert'],
    "manager_states.ACTIVE": ["is running", "läuft"],
    "manager_states.STARTING": ["is starting", "startet"],
    "manager_states.RESTARTING": ["is restarting", "startet neu"],
    "manager_states.UPDATING": ["is being updated", "wird aktualisiert"],
    "manager_states.UPDATING_OS": ["is updating the OS", "aktualisiert OS"],
    "manager_states.INACTIVE": ["is not running", "läuft nicht"],
    "search": ["Search", "Suchen"]
}

manager_state = None

clock = None
user_cb = None
greeter = None
login_clicked = False
password_entry = None
password_label = None
status_label = None
status_spinner = None
reboot_label = None
manager_label = None
manager_icon = None
ip_label = None

lang_code = None
login_no = 0

layout_search = None
layout_tree = None
layout_choose = None
layout_short = None
layout_text = None
layoutStore = Gtk.ListStore(str)

lang_button_en = None
lang_button_de = None

second_window = None

builder = None

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
    global current_lang
    current_lang = lang

    label_lang_text      = get_translation_text("label_lang", lang)
    label_keyboard_text  = get_translation_text("label_keyboard", lang)
    label_user_text      = get_translation_text("label_user", lang)
    password_label_text  = get_translation_text("password_label", lang)
    label_manager_text   = get_translation_text("label_manager", lang)
    login_button_text    = get_translation_text("login_button", lang)
    reboot_button_text   = get_translation_text("reboot_button", lang)
    poweroff_button_text = get_translation_text("poweroff_button", lang)

    builder.get_object("label_lang").set_text(label_lang_text)
    builder.get_object("label_keyboard").set_text(label_keyboard_text)
    builder.get_object("label_user").set_text(label_user_text)
    builder.get_object("password_label").set_text(password_label_text)
    builder.get_object("label_manager").set_text(label_manager_text)
    builder.get_object("login_button").set_label(login_button_text)
    builder.get_object("reboot_button").set_label(reboot_button_text)
    builder.get_object("poweroff_button").set_label(poweroff_button_text)

    translate_manager_state()

    current_layout = cache.get("greeter", "last-layout", fallback="English (US)")
    layout_choose.set_label(str(layout_short))
    layout_choose.set_tooltip_text(str(layout_text))

    load_reboot_required()
    load_ip()


def get_translation_text(key, lang, default=None):
    index = 1 if lang == "de" else 0

    if key in translation:
        return translation[key][index]
    elif default is not None:
        return default
    else:
        return str(key)


def translate_manager_state():
    if manager_state is None: return

    manager_state_text = get_translation_text(
            f'manager_states.{manager_state}', current_lang, manager_state)
    builder.get_object("manager_state_label").set_text(manager_state_text)


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
    users = LightDM.UserList().get_instance().get_users()

    for id, user in enumerate(users):
        user_cb.append_text(user.get_name())
        if user.get_name() == last_user:
            user_id = id

    user_cb.set_active(user_id)


def fill_layout_store():
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


def set_layout(layout_text_):
    global layout_short
    global layout_text

    layout_obj = None

    for layout in LightDM.get_layouts():
        if layout.get_description().upper() == layout_text_.upper():
            layout_obj = layout
            break

    if layout_obj is None:
        return

    layout_short = layout_obj.get_name().split("\t")[0].upper()
    layout_text = layout_obj.get_description()

    cache.set("greeter", "last-layout", layout_obj.get_description())

    LightDM.set_layout(layout_obj)


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
    global login_clicked, login_no
    login_clicked = True
    login_no += 1

    if greeter.get_is_authenticated():
        start_session()

    if greeter.get_in_authentication():
        greeter.cancel_authentication()

    status_label.set_text(
        get_translation_text("status.login", current_lang)
    )
    status_spinner.show()
    status_spinner.start()

    username = user_cb.get_active_text()
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
    status_label.set_text(text)


def display_error_message(text, duration=5000):
    status_label.set_text(
        get_translation_text("status.login_failed", current_lang)
    )
    status_spinner.hide()

    local_login_no = login_no

    def inner():
        global login_no
        if local_login_no != login_no:
            return False

        status_label.set_text("")
        return False

    GLib.timeout_add(duration, inner)


def set_manager_state():
    if manager_label is None: return False

    global manager_state

    try:
        resp = requests.get(SERVER_STATUS_URL, allow_redirects=False)

        if resp.text == "UP":
            state = "ACTIVE"
        else:
            state = resp.text
    except requests.exceptions.ConnectionError:
        state = "INACTIVE"
    finally:
        manager_label.set_text(state)
        manager_state = state

        if state == "ACTIVE":
            manager_icon.set_from_icon_name("gtk-yes", manager_icon.get_icon_name()[1])
        else:
            manager_icon.set_from_icon_name("view-refresh", manager_icon.get_icon_name()[1])

        translate_manager_state()
    return True


def show_layout_chooser(*_):
    global layout_tree
    global second_window

    builder2 = Gtk.Builder()
    builder2.add_from_file(UI_LAYOUT_CHOOSER_FILE_LOCATION)

    fill_layout_store()

    layout_tree = builder2.get_object("tree")
    layout_tree.set_search_entry(builder2.get_object("search"))
    layout_tree.set_model(layoutStore)
    tree_column = Gtk.TreeViewColumn("", Gtk.CellRendererText(), text=0)
    layout_tree.append_column(tree_column)
    layout_tree.set_expander_column(tree_column)

    layout_tree.connect("row-activated", handle_set_layout)

    button_choose = builder2.get_object("button_choose")
    button_choose.connect("clicked", handle_set_layout)

    button_cancel = builder2.get_object("button_cancel")
    button_cancel.connect("clicked", lambda _ : second_window.close())

    layout_search = builder2.get_object("search")
    layout_search.connect("activate", handle_set_layout)


    second_window = builder2.get_object("window")
    second_window.set_modal(True)
    second_window.resize(second_window.get_size()[0], screen.get_height() * 0.8)

    vertical_center_position = (screen.get_width() / 2) - (second_window.get_size()[0] / 2)
    second_window.move(vertical_center_position, screen.get_height() * 0.1)
    second_window.show()


def handle_set_layout(*_):
    cursor = layout_tree.get_cursor()

    if cursor[0] is None:
        return

    index = cursor[0].get_indices()[0]

    layout_text = list(layout_tree.get_model()[index])[0]

    set_layout(layout_text)

    second_window.close()
    layout_choose.set_label(f"{layout_short}")
    layout_choose.set_tooltip_text(f"{layout_text}")


def button_en_clicked(_):
    if lang_button_en.get_active() == True:
        lang_button_de.set_active(False)
    elif lang_button_de.get_active() == False:
        lang_button_en.set_active(True)
        return

    language_change_handler("en")


def button_de_clicked(_):
    if lang_button_de.get_active() == True:
        lang_button_en.set_active(False)
    elif lang_button_en.get_active() == False:
        lang_button_de.set_active(True)
        return

    language_change_handler("de")


def language_change_handler(lang="en"):
    global lang_code

    lang_code = "de_DE.utf8" if lang == "de" else "en_US.utf8"
    cache.set("greeter", "last-lang", lang_code)

    if lang_code == "de_DE.utf8":
        set_language("de")
    elif lang_code == "en_US.utf8":
        set_language("en")


def load_reboot_required():
    if current_lang == "de":
        cmd = "LANG=de_DE.UTF-8 tcos-reboot-required"
    else:
        cmd = "LANG=en_US.UTF-8 tcos-reboot-required"

    process = subprocess.run(cmd, capture_output=True, shell=True)
    message = process.stdout.decode().strip()
    reboot_label.set_text(message)
        

def load_ip():
    if current_lang == "de":
        cmd = "LANG=de_DE.UTF-8 tcos-ip"
    else:
        cmd = "LANG=en_US.UTF-8 tcos-ip"
    process = subprocess.run(cmd, capture_output=True, shell=True)
    ip = process.stdout.decode().strip()
    ip_label.set_text(ip)


if __name__ == "__main__":
    builder = Gtk.Builder()
    greeter = LightDM.Greeter()
    greeter.connect("authentication-complete", authentication_complete)
    greeter.connect("show-prompt", show_prompt)
    greeter.connect("show-message", show_message)

    cursor = Gdk.Cursor(Gdk.CursorType.LEFT_PTR)
    builder.add_from_file(UI_FILE_LOCATION)

    cssProvider = Gtk.CssProvider()
    cssProvider.load_from_path(CSS_FILE_LOCATION)
    styleContext = Gtk.StyleContext()
    screen = Gdk.Screen.get_default()

    styleContext.add_provider_for_screen(
        screen,
        cssProvider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    poweroffButton = builder.get_object("poweroff_button")
    poweroffButton.connect("activate", poweroff_click_handler)

    rebootButton = builder.get_object("reboot_button")
    rebootButton.connect("activate", reboot_click_handler)

    password_entry = builder.get_object("password_entry")
    password_entry.connect("activate", login_click_handler)
    password_label = builder.get_object("password_label")

    status_label = builder.get_object("status_label")
    status_spinner = builder.get_object("status_spinner")

    loginButton = builder.get_object("login_button")
    loginButton.connect("clicked", login_click_handler)

    user_cb = builder.get_object("user_cb")
    user_cb.connect("changed", user_change_handler)
    fill_with_users(user_cb)

    layout_choose = builder.get_object("layout_choose")
    layout_choose.connect("clicked", show_layout_chooser)

    layout = cache.get("greeter", "last-layout", fallback="English (US)")
    set_layout(layout)
    del layout

    ip_label = builder.get_object("ip_label")

    lang_button_de = builder.get_object("button_de")
    lang_button_de.connect("clicked", button_de_clicked)
    lang_button_en = builder.get_object("button_en")
    lang_button_en.connect("clicked", button_en_clicked)

    reboot_label = builder.get_object("reboot_label")
    load_reboot_required()
    GLib.timeout_add(30000, load_reboot_required)

    lang_code = cache.get("greeter", "last-lang", fallback="en_US.utf8")
    if lang_code == "de_DE.utf8":
        lang_button_de.set_active(True)
        set_language("de")
    else:
        lang_button_en.set_active(True)
        set_language("en")

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

    GLib.timeout_add(100, lambda *_ : user_change_handler(None) and False)

    GLib.MainLoop().run()
