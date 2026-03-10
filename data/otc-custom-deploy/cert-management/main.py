import os
from pathlib import Path
from subprocess import Popen
import subprocess
import pam
from functools import wraps
from flask import Flask, redirect, render_template, request, send_file
from fluent.runtime import FluentLocalization, FluentResourceLoader

CADDY_PKI_DIR = Path("/var/lib/caddy/.local/share/caddy/pki/authorities/local/")
USER_CERT_PATH = Path("/var/lib/caddy/user.crt")
USER_KEY_PATH = Path("/var/lib/caddy/user.key")

TEMP_CERT_PATH = Path("/var/lib/caddy/temp.crt")
TEMP_KEY_PATH = Path("/var/lib/caddy/temp.key")

SSL_CONFIG_PATH = Path("/etc/caddy/ssl_config")

ALLOWED_SSL_HOSTS = (
    ['localhost', '172.0.0.1', '::1', '::'] +
    subprocess.run(['hostname', '-I'],
                   capture_output=True).stdout.decode().split() +
    subprocess.run(['hostname', '-A'],
                   capture_output=True).stdout.decode().split()
)

app = Flask(__name__)
loader = FluentResourceLoader("l10n/{locale}")

class InvalidCertError(Exception):
    pass


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

def translated_view(f):
    @wraps(f)
    def wrapped_view(**kwargs):
        langs = [lang for lang,_weight in request.accept_languages]
        langs.append("en")
        l10n = FluentLocalization(langs, ["main.ftl"], loader)
        return f(l10n=l10n, **kwargs)
    return wrapped_view

@app.route("/")
@translated_view
def main_page(l10n):
    return render_template("index.html", tr=l10n.format_value,
                           using_internal_cert=not USER_CERT_PATH.exists())

@app.route("/download_cert")
def download_cert():
    return send_file(CADDY_PKI_DIR / "root.crt")

def check_cert_key():
    cert_process = subprocess.run(['openssl', 'x509', '-in',
                                  TEMP_CERT_PATH, '-modulus', '-noout'],
                                  capture_output=True)
    key_process = subprocess.run(['openssl', 'rsa', '-noout', '-modulus', '-in',
                                 TEMP_KEY_PATH], capture_output=True)

    if cert_process.returncode:
        raise InvalidCertError('cert_wrong_format')
    if key_process.returncode:
        raise InvalidCertError('key_wrong_format')

    if str(key_process.stdout) != str(cert_process.stdout):
        raise InvalidCertError('cert_key_missmatch')

@app.route("/upload_cert", methods=['POST'])
@login_required
@translated_view
def upload_cert(l10n):
    def render_error_page(error):
        return render_template('error.html', error=l10n.format_value(error),
                               tr=l10n.format_value)

    if 'cert' not in request.files or 'key' not in request.files:
        return render_error_page('files_not_uploaded')
    cert = request.files['cert']
    key = request.files['key']
    if cert.filename == '' or key.filename == '':
        return render_error_page('files_not_uploaded')

    cert.save(TEMP_CERT_PATH)
    key.save(TEMP_KEY_PATH)

    try:
        check_cert_key()
    except InvalidCertError as e:
        return render_error_page(e.args[0])

    os.rename(TEMP_CERT_PATH, USER_CERT_PATH)
    os.rename(TEMP_KEY_PATH, USER_KEY_PATH)

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

@app.route(rule="/is_domain_allowed")
def is_domain_allowed():
    if request.args.get('domain') in ALLOWED_SSL_HOSTS:
        return "yes"
    return ('Forbidden', 403, {})
