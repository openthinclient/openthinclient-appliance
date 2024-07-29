from http.server import BaseHTTPRequestHandler
import json

class WizardServer(BaseHTTPRequestHandler):
    endpoints = {}

    @staticmethod
    def endpoint(route, methods=["GET"]):
        def inner(func):
            WizardServer.endpoints['/'+route] = {"f": func, "methods": methods}

        return inner

    def route(self, path, method = "GET", data=None):
        route_spec = WizardServer.endpoints.get(path, None)

        if route_spec is None:
            route_spec = WizardServer.endpoints.get("/*", None)

        if route_spec is None:
            self.not_found()
        else:
            if method in route_spec["methods"]:
                if data != None:
                    route_spec["f"](self, data)
                else:
                    route_spec["f"](self)
            else:
                self.wrong_method()

    def not_found(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Not Found\n")

    def wrong_method(self):
        self.send_response(405)
        self.end_headers()

    def respond(self, code, headers, json_data):
        self.send_response(code)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(json_data), "utf-8"))
        self.wfile.write(b"\n")

    def do_GET(self):
        self.route(self.path)

    def do_POST(self):
        data = None
        if self.headers["Content-Type"] == "application/json":
            length = int(self.headers['Content-Length'])
            try:
                data = json.loads(self.rfile.read(length))
            except json.decoder.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                return

        self.route(self.path, method="POST", data=data)

def needs_data(f):
    def inner(server, data=None):
        if data is None:
            server.respond(
                400,
                {"Content-Type": "application/json"},
                {"successful": False}
            )
        else:
            f(server, data)

    return inner
