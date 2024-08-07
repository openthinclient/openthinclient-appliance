import './style.scss'

import { next, back, goto } from './src/navigation.js'
import { quit } from './src/quit.js'
import { set_appliance_password, set_management_password, set_timezone, set_proxy, clear_errors } from './src/actions.js'
import { inject_logo } from './src/inject_logo.js'
import { inject_timezones } from './src/inject_timezones.js'
import { setup_handlers } from './src/setup_handlers.js'
import { set_lang, t, translate_all } from './src/translation.js'
import { set_default_mode, update_form as update_proxy_form } from './src/proxy_form.js'

inject_logo()
inject_timezones()

if(import.meta.env.DEV) {
  window.wizard_dev = {
    "next": next,
    "back": back,
    "goto": goto,
    "quit": quit,
    "actions": {
      "set_password": set_appliance_password,
      "set_timezone": set_timezone,
      "clear_errors": clear_errors
    },
    "translation": {
      "t": t,
      "set_lang": set_lang,
      "translate_all": translate_all
    }
  }
}

let lang = navigator.language.split("-")[0].toLowerCase()
document.getElementById("lang").value = lang
set_lang(lang)
translate_all()

setup_handlers(next, back, quit, set_appliance_password, set_management_password, set_timezone, set_proxy, set_lang, update_proxy_form)
set_default_mode()
