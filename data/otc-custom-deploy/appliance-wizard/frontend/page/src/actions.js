import { next } from './navigation.js';
import { t } from './translation.js';

export function set_appliance_password() {
  const pw = document.getElementById("appliance-pass").value;
  const pw_check = document.getElementById("appliance-pass_check").value;

  document.getElementById("appliance-pass-err").innerText = "";

  if (pw.length < 8) {
    document.getElementById("appliance-pass-err").innerText = t("err.password_too_short");
    document.getElementById("appliance-pass_check").value = "";
    return;
  }

  if (pw != pw_check) {
    document.getElementById("appliance-pass-err").innerText = t("err.password_unequal");
    document.getElementById("appliance-pass_check").value = "";
    return;
  }

  do_post("http://localhost:4321/api/v1/password", {"password": pw}).then(res => {
    return res.json();
  }).then(data => {
    if (data["successful"] == true) {
      next()
    } else {
      document.getElementById("appliance-pass-err").innerHTML = t("err.password_unable_to_set");
    }
  }).catch(e => {
    console.log(e);
    document.getElementById("appliance-pass-err").innerHTML = t("err.password_unable_to_set");
  });
}

export function set_management_password() {
  const pw = document.getElementById("management-pass").value;
  const pw_check = document.getElementById("management-pass_check").value;

  document.getElementById("management-pass-err").innerText = "";

  if (pw.length < 8) {
    document.getElementById("management-pass-err").innerText = t("err.password_too_short");
    document.getElementById("management-pass_check").value = "";
    return;
  }

  if (pw != pw_check) {
    document.getElementById("management-pass-err").innerText = t("err.password_unequal");
    document.getElementById("management-pass_check").value = "";
    return;
  }

  const submit_button = document.getElementById("management-password-submit")
  submit_button.disabled = true;

  do_post("http://localhost:4321/api/v1/password_management", {"password": pw}).then(res => {
    submit_button.disabled = false;
    return res.json();
  }).then(data => {
    if (data["successful"] == true) {
      next()
    } else {
      document.getElementById("management-pass-err").innerHTML = t("err.password_unable_to_set");
    }
  }).catch(e => {
    submit_button.disabled = false;
    console.log(e);
    document.getElementById("management-pass-err").innerHTML = t("err.password_unable_to_set");
  });
}

export function set_timezone() {
  const zone = document.getElementById("timezone-select").value;

  do_post("http://localhost:4321/api/v1/timezone", {"timezone": zone}).then(res => {
    return res.json();
  }).then(data => {
    if (data["successful"] == true) {
      next()
    } else {
      document.getElementById("zone-err").innerHTML = t("err.timezone_unable_to_set");
    }
  }).catch(e => {
    console.log(e);
    document.getElementById("zone-err").innerHTML = t("err.timezone_unable_to_set");
  })
}

export function set_proxy() {
  const mode = document.getElementById("proxy_mode_select").value;

  let promises = [];

  promises.push(
    do_post("http://localhost:4321/api/v1/proxy/mode", {"mode": mode})
  );

  switch (mode) {
    case ("manual"): {
      var http_host = document.getElementById("proxy_http_host").value;
      var http_port = document.getElementById("proxy_http_port").value;
      var https_host = document.getElementById("proxy_https_host").value;
      var https_port = document.getElementById("proxy_https_port").value;
      var ftp_host = document.getElementById("proxy_ftp_host").value;
      var ftp_port = document.getElementById("proxy_ftp_port").value;
      var socket_host = document.getElementById("proxy_socket_host").value;
      var socket_port = document.getElementById("proxy_socket_port").value;

      console.log({
        "http_host":http_host,
        "http_port":http_port,
        "https_host":https_host,
        "https_port":https_port,
        "ftp_host":ftp_host,
        "ftp_port":ftp_port,
        "socket_host":socket_host,
        "socket_port":socket_port});

      promises.join([
        do_post("http://localhost:4321/api/v1/proxy/manual/http", {"host": http_host, "port": http_port}),
        do_post("http://localhost:4321/api/v1/proxy/manual/https", {"host": https_host, "port": https_port}),
        do_post("http://localhost:4321/api/v1/proxy/manual/ftp", {"host": ftp_host, "port": ftp_port}),
        do_post("http://localhost:4321/api/v1/proxy/manual/socks", {"host": socket_host, "port": socket_port}),
      ]);
    }

    case ("auto"): {
      var address = document.getElementById("proxy_auto_address").value;

      promises.push(
        do_post("http://localhost:4321/api/v1/proxy/autoconfig", {"autoconfig": address})
      );
    }
  }

  console.log({"p": promises});

  Promise.all(promises)
    .then(() => {
      console.log("saved")
      next()
    })
    .catch(err => {
      console.log(err)
    });

  console.log(mode);
}

export function clear_errors() {
  document.querySelectorAll(".err").forEach((item, i) => {
    item.innerText = "";
  });

}

function do_post(url, body) {
  return fetch(
    url,
    {
      "method": "POST",
      "body": JSON.stringify(body),
      "headers": {
        "Content-Type": "application/json"
      }
    }
  )
}
