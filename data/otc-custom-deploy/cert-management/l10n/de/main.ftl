cert_status_header = Zurzeit verwendetes Zertifikat
upload_cert_header = Zertifikat hochladen
upload_cert_help_text = Laden Sie ein Zertifikat und den zugehörigen privaten Schlüssel hoch. Das Zertifikat muss für die URL gültig sein, mit der das openthinclient-Management erreichbar sein soll.
certificate_label = Zertifikat
key_label = Zertifikatsschlüssel
submit_label = Hochladen
download = Herunterladen
provided_cert = Hochgeladenes Zertifikat wird verwendet.
delete = Löschen
page_title = openthinclient Zertifikatsmanagement
confirm_cert_deletion = Hochgeladenes Zertifikat wirklich löschen?
login_hint = Nutzen Sie die Zugangsdaten der openthinclient Appliance um ein Zertifikat hochzuladen.

files_not_uploaded = Fehler: Bitte laden sie Zertifikat und Schlüssel hoch.
cert_wrong_format = Fehler: Das hochgeladene Zertifikat hat nicht das richtige format. Bitte laden sie ein SSL-Zertifikat im PEM-Format hoch.
key_wrong_format = Fehler: Der hochgeladene Schlüssel hat nicht das richtige format. Bitte laden sie einen OpenSSL private key hoch.
cert_key_missmatch = Fehler: Der hochgeladene Schlüssel und das Zertifikat passen nicht zusammen.
communication_failed = Fehler: Die Kommunikation mit dem Backend ist fehlgeschlagen. Bitte laden sie diese Seite neu.

internal_cert_header = Erzeugtes Zertifikat wird verwendet
provided_cert_header = Hochgeladenes Zertifikat wird verwendet
issued_certs = Ausgestellte Zertifikate
issued_certs_explainer = Zertifikate werden automatisch ausgestellt, wenn das openthinclient-Management oder das Zertifikatsmanagement aufgerufen wird. Die Zertifikate werden nur für die IP-Adressen und den Hostnamen der openthinclient Appliance ausgestellt.
confirm_issued_cert_deletion = Zertifikat wirklich löschen?
cert_subject = Betreff
cert_name = Host
cert_fingerprint = SHA256-Fingerabdruck

cert_management_settings = Einstellungen
reachability_setting = Zertifikatsmanagement nur auf der Appliance erreichbar
reachability_setting_explainer = Wenn diese Option aktiviert ist, ist das Zertifikatsmanagement nur lokal auf der Appliance erreichbar. Ist die Option deaktiviert, kann das Zertifikatsmanagement auch aus dem Netzwerk aufgerufen werden.
https_setting = HTTPS aktiviert
https_setting_explainer = Wenn diese Option aktiviert ist, werden Verbindungen zum openthinclient-Management per HTTPS gesichert. Aufrufe über Port 8080 werden automatisch auf Port 443 umgeleitet.
settings_save_label = Anwenden
confirm_set_settings = Einstellungen anwenden?\n\nWenn sie die erreichbarkeit nur auf der Appliance aktiviert haben, wird diese Seite dann nur noch auf der openthinclient Appliance erreichbar sein.

confirm_title = Bitte bestätigen
docs_hint_pre = Mehr Informationen finden sie in unserer
docs_link = Dokumentation
