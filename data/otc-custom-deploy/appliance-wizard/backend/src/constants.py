BUFFER_SIZE = 512

HOST = "localhost"
PORT =  4321

PROXY_HTTP_OPTION_KEYS  = [
    "host",
    "port",
    "use-authentication",
    "authentication-user",
    "authentication-password"
]
PROXY_HTTPS_OPTION_KEYS = ["host", "port"]
PROXY_FTP_OPTION_KEYS   = ["host", "port"]
PROXY_SOCKS_OPTION_KEYS = ["host", "port"]

PID_FILE_PATH = "/var/run/user/1000/appliance-wizard-frontend.pid"
