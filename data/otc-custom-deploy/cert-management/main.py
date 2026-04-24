import shutil
import pam
import subprocess
from flask.json import jsonify
from flask import Flask, Response, redirect, render_template, request, send_file
from fluent.runtime import FluentLocalization, FluentResourceLoader
from functools import wraps
from pathlib import Path

CADDY_DATA = Path("/var/lib/caddy/.local/share/caddy/")
CADDY_PKI_DIR = CADDY_DATA / 'pki' / 'authorities' / 'local'
CADDY_CERTS_DIR = CADDY_DATA / 'certificates' / 'local'
USER_CERT_PATH = Path("/var/lib/caddy/user.crt")
USER_KEY_PATH = Path("/var/lib/caddy/user.key")

TEMP_CERT_PATH = Path("/var/lib/caddy/temp.crt")
TEMP_KEY_PATH = Path("/var/lib/caddy/temp.key")

SSL_CONFIG_PATH = Path("/etc/caddy/ssl_config")
CADDY_CONFIG_DIR = Path("/etc/caddy")

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


def reload_caddy():
    subprocess.run(['systemctl', 'reload', 'caddy'])

def login_required(view_fn):
    @wraps(view_fn)
    def wrapped_view(**kwargs):
        auth = request.authorization
        if not (auth and pam.authenticate(auth.username, auth.password)):
            return ('Unauthorized', 401, {
                'WWW-Authenticate':
                'Basic realm="Login using openthinclient-Appliance credentials"'
            })

        return view_fn(**kwargs)
    return wrapped_view

def translated_view(view_fn):
    @wraps(view_fn)
    def wrapped_view(**kwargs):
        langs = [lang for lang,_weight in request.accept_languages]
        langs.append('en')
        l10n = FluentLocalization(langs, ['main.ftl'], loader)
        return view_fn(l10n=l10n, **kwargs)
    return wrapped_view

def get_cert_info(cert_path):
    try:
        openssl_out = subprocess.run(
            ['openssl', 'x509', '-in', cert_path, '-noout', '-subject',
                                '-fingerprint', '-sha256'],
            capture_output=True
        )
        subject, fingerprint, *_ = openssl_out.stdout.decode().splitlines()
        openssl_out = subprocess.run(
            ['openssl', 'x509',  '-in', cert_path, '-noout',
                                 '-ext', 'subjectAltName'],
            capture_output=True
        )
        openssl_out = openssl_out.stdout.decode()
        name = None
        if "Subject Alternative Name" in openssl_out:
            name = openssl_out.splitlines()[1].split(":", 1)[1]

        return (
            subject.split('=', 1)[1],
            fingerprint.split('=')[1].replace(":", ":<wbr>"),
            name
        )
    except Exception as e:
        print(e)
        return None

@app.route("/")
@translated_view
def main_page(l10n):
    if ((CADDY_CONFIG_DIR / 'cert_management').readlink()
        .name.endswith('extern')):
        externally_reachable = True
    else:
        externally_reachable = False
    using_user_cert = USER_CERT_PATH.exists()
    cert_path = (USER_CERT_PATH if using_user_cert else
                 CADDY_PKI_DIR / 'root.crt')
    cert_subject, cert_fingerprint, cert_name = (get_cert_info(cert_path)
                                                 or ("cert not found", "", ""))
    generated_cert_infos = []
    if not using_user_cert:
        for cert_dir in CADDY_CERTS_DIR.iterdir():
            cert_path = cert_dir / f"{cert_dir.name}.crt"
            if not cert_path.exists():
                return
            if cert_info := get_cert_info(cert_path):
                generated_cert_infos.append((cert_dir.name, *cert_info[1:]))

    return render_template("index.html", tr=l10n.format_value,
                           externally_reachable=externally_reachable,
                           cert_subject=cert_subject,
                           cert_fingerprint=cert_fingerprint,
                           cert_name=cert_name,
                           using_internal_cert=not using_user_cert,
                           generated_cert_infos=generated_cert_infos)

@app.route("/download_cert")
def download_cert():
    if USER_CERT_PATH.exists():
        return send_file(USER_CERT_PATH)
    return send_file(CADDY_PKI_DIR / 'root.crt')

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
    def render_error_page(err_key):
        response = jsonify(error=l10n.format_value(err_key))
        response.status_code = 400
        return response

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
    except InvalidCertError as exc:
        return render_error_page(exc.args[0])

    TEMP_CERT_PATH.rename(USER_CERT_PATH)
    TEMP_KEY_PATH.rename(USER_KEY_PATH)

    SSL_CONFIG_PATH.write_text(f"tls {USER_CERT_PATH} {USER_KEY_PATH}\n")
    reload_caddy()
    return Response(status=204)

@app.route(rule="/delete_cert")
@login_required
def delete_cert():
    USER_CERT_PATH.unlink()
    USER_KEY_PATH.unlink()

    SSL_CONFIG_PATH.write_text("tls internal {\non_demand\n}\n")
    reload_caddy()
    return redirect("/")

@app.route(rule="/delete_issued_cert/<string:cert_name>")
def delete_issued_cert(cert_name: str):
    shutil.rmtree(CADDY_CERTS_DIR / cert_name)
    reload_caddy()
    return redirect("/")

@app.route(rule="/set_reachability_external")
@login_required
def set_reachability_external():
    (CADDY_CONFIG_DIR / 'cert_management').unlink(True)
    (CADDY_CONFIG_DIR / 'cert_management').symlink_to(
        CADDY_CONFIG_DIR / 'blocks' / 'cert_management_extern'
    )
    reload_caddy()
    return redirect("/")

@app.route(rule="/set_reachability_local")
@login_required
def set_reachability_local():
    (CADDY_CONFIG_DIR / 'cert_management').unlink(True)
    (CADDY_CONFIG_DIR / 'cert_management').symlink_to(
        CADDY_CONFIG_DIR / 'blocks' / 'cert_management_local'
    )
    reload_caddy()
    return redirect("/")

@app.route(rule='/enable_https')
@login_required
def enable_https():
    (CADDY_CONFIG_DIR / 'Caddyfile').unlink(True)
    (CADDY_CONFIG_DIR / 'Caddyfile').symlink_to(
        CADDY_CONFIG_DIR / 'blocks' / 'Caddyfile_https'
    )
    reload_caddy()
    return redirect('/')

@app.route(rule='/disable_https')
@login_required
def disable_https():
    (CADDY_CONFIG_DIR / 'Caddyfile').unlink(True)
    (CADDY_CONFIG_DIR / 'Caddyfile').symlink_to(
        CADDY_CONFIG_DIR / 'blocks' / 'Caddyfile_http'
    )
    reload_caddy()
    return redirect('/')

@app.route(rule="/is_domain_allowed")
def is_domain_allowed():
    if request.args.get('domain') in ALLOWED_SSL_HOSTS:
        return "yes"
    return ('Forbidden', 403, {})
