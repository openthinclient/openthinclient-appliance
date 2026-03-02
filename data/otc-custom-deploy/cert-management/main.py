from pathlib import Path
from subprocess import Popen
import pam
from functools import wraps
from flask import Flask, redirect, render_template, request, send_file
from fluent.runtime import FluentLocalization, FluentResourceLoader

CADDY_PKI_DIR = Path("/var/lib/caddy/.local/share/caddy/pki/authorities/local/")
USER_CERT_PATH = Path("/var/lib/caddy/user.crt")
USER_KEY_PATH = Path("/var/lib/caddy/user.key")

SSL_CONFIG_PATH = Path("/etc/caddy/ssl_config")

app = Flask(__name__)
loader = FluentResourceLoader("l10n/{locale}")

def login_required(f):
    @wraps(f)
    def wrapped_view(**kwargs):
        auth = request.authorization
        if not (auth and pam.authenticate(auth.username, auth.password)):
            return ('Unauthorized', 401, {
                'WWW-Authenticate': 'Basic realm="Login Required"'
            })

        return f(**kwargs)
    return wrapped_view

@app.route("/")
def main_page():
    langs = [lang for lang,_weight in request.accept_languages]
    langs.append("en")
    l10n = FluentLocalization(langs, ["main.ftl"], loader)

    print(USER_CERT_PATH.exists())
    return render_template("index.html", tr=l10n.format_value,
                           using_internal_cert=not USER_CERT_PATH.exists())

@app.route("/download_cert")
def download_cert():
    return send_file(CADDY_PKI_DIR / "root.crt")

@app.route("/upload_cert", methods=['POST'])
@login_required
def upload_cert():
    if 'cert' not in request.files or 'key' not in request.files:
        return "required files not uploaded"
    cert = request.files['cert']
    key = request.files['key']
    if cert.filename == '' or key.filename == '':
        return "required files not selected"

    cert.save(USER_CERT_PATH)
    key.save(USER_KEY_PATH)

    SSL_CONFIG_PATH.open('w').write(f"""\
tls {USER_CERT_PATH} {USER_KEY_PATH}
""")
    Popen(['/usr/bin/sh', '-c', 'sleep 1; systemctl reload caddy'])
    return redirect("/")


@app.route(rule="/delete_cert")
@login_required
def delete_cert():
    USER_CERT_PATH.unlink()
    USER_KEY_PATH.unlink()

    SSL_CONFIG_PATH.open('w').write("""\
tls internal {
    on_demand
}
""")
    Popen(['/usr/bin/sh', '-c', 'sleep 1; systemctl reload caddy'])
    return redirect("/")
