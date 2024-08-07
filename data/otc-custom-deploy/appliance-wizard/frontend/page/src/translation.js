import t_json from './translations.json';
import { clear_errors } from './actions.js';

var lang_code = null

export function set_lang(l) {
  if (l != "de") {
    lang_code = "en";
  } else {
    lang_code = "de";
  }

  translate_all()
}

export function t(key) {
  let text = t_json[lang_code][key];

  if (text == undefined) {
    return key;
  }

  return text;
}

export function translate_all() {
  clear_errors();
  document.querySelectorAll("[i18n]").forEach((item, i) => {
    item.innerHTML = t(item.getAttribute("i18n"))
  });

  document.querySelectorAll("[i18n-placeholder]").forEach((item, i) => {
    item.setAttribute(
      "placeholder",
      t(item.getAttribute("i18n-placeholder"))
    )
  })
}
