export function set_default_mode() {
  let proxy_mode_select = document.getElementById("proxy_mode_select");
  proxy_mode_select.value = proxy_mode_select.getAttribute("default");

  update_form()
}


export function update_form() {
  let mode = document.getElementById("proxy_mode_select").value;

  document.querySelectorAll("#proxy_dynamic_form [proxy_mode_form]").forEach((item, i) => {
    item.style.display = 'none';
  });

  switch (mode) {
    case 'manual':
      document.querySelector("#proxy_dynamic_form [proxy_mode_form=\"manual\"]")
        .style.display = '';
      break;

    case 'auto':
      document.querySelector("#proxy_dynamic_form [proxy_mode_form=\"auto\"]")
        .style.display = '';
  }
}
