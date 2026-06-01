cert_status_header = Currently used certificate
upload_cert_header = Upload certificate
upload_cert_help_text = Upload a certificate and the corresponding private key. The certificate must be valid for the URL used to access openthinclient-Management.
certificate_label = Certificate
key_label = Certificate key
submit_label = Upload
download = Download
provided_cert = Uploaded certificate is in use.
delete = Delete
page_title = openthinclient Certificate Management
confirm_cert_deletion = Are you sure you want to delete the uploaded certificate?
login_hint = To upload a certificate, use the login credentials of the openthinclient appliance.

files_not_uploaded = Error: Please upload certificate and key.
cert_wrong_format = Error: The uploaded certificate is not in the correct format. Please upload an SSL certificate in PEM format.
key_wrong_format = Error: The uploaded key is not in the correct format. Please upload an OpenSSL private key.
cert_key_missmatch = Error: The uploaded key and certificate do not match.
communication_failed = Error: Could not contact the backend. Please reload this page.

internal_cert_header = Generated certificate in use
provided_cert_header = Uploaded certificate in use
issued_certs = Issued certificates
issued_certs_explainer = Certificates are issued automatically when the openthinclient-Management or the certificate management is accessed. Certificates are issued only for the IP addresses and hostname of the openthinclient Appliance.
confirm_cert_deletion = Are you sure you want to delete certificate?
cert_subject = Subject
cert_name = Host
cert_fingerprint = SHA256-Fingerprint

cert_management_settings = Settings
reachability_setting = Certificate management is accessible only on the appliance
reachability_setting_explainer = When this option is enabled, the certificate management is accessible only locally on the appliance. When the option is disabled, the certificate management can also be accessed from the network.
https_setting = HTTPS Enabled
https_setting_explainer = When this option is enabled, connections to the openthinclient-Management are secured using HTTPS. Requests to port 8080 are automatically redirected to port 443.
settings_save_label = Apply
confirm_set_settings = Apply settings?\n\nIf you have enabled certificate management is only accessible on the appliance, this page will then only be accessible on the openthinclient appliance.

confirm_title = Please confirm
docs_hint_pre = For more information, see our
docs_link = documentation
