export function setup_handlers(next, back, quit, set_appliance_password, set_management_password, set_timezone, set_proxy, set_lang, update_proxy_form) {
  document.querySelectorAll('[action="next"]').forEach((item, i) => {
    item.onclick = next;
  });

  document.querySelectorAll('[action="back"]').forEach((item, i) => {
    item.onclick = back;
  });

  document.querySelectorAll('[action="quit"]').forEach((item, i) => {
    item.onclick = quit;
  });


  document.querySelectorAll('[action="set_appliance_password"]').forEach((item, i) => {
    let f = () => {
      set_appliance_password();
      return false;
    };

    if(item.tagName == "FORM") {
      item.onsubmit = f;
    } else {
      item.onclick = f;
    }
  });

  document.querySelectorAll('[action="set_management_password"]').forEach((item, i) => {
    let f = () => {
      set_management_password();
      return false;
    };

    if(item.tagName == "FORM") {
      item.onsubmit = f;
    } else {
      item.onclick = f;
    }
  });

  document.querySelectorAll('[action="set_timezone"]').forEach((item, i) => {
    let f = () => {
      set_timezone();
      return false;
    };

    if(item.tagName == "FORM") {
      item.onsubmit = f;
    } else {
      item.onclick = f;
    }
  });

  document.querySelectorAll('[action="set_proxy"]').forEach((item, i) => {
    let f = () => {
      set_proxy();
      return false;
    };

    if(item.tagName == "FORM") {
      item.onsubmit = f;
    } else {
      item.onclick = f;
    }
  });

  document.querySelectorAll('[lang="select"]').forEach((item, i) => {
    item.onchange = () => {
      set_lang(item.value)
    };
  });

  document.querySelectorAll('[action="update_proxy_form"]').forEach((item, i) => {
    item.onchange = update_proxy_form;
  });
}
