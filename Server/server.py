from http.server import BaseHTTPRequestHandler, HTTPServer
from os import environ
import time
import json

hostName = environ.get("host") or "0.0.0.0"
serverPort = int(environ.get("port") or 8080)


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            self.route()
        except Exception as e:
            self.send_error(500, str(e))
            print(e)
            e.with_traceback()

    def do_POST(self):
        try:
            self.route()
        except Exception as e:
            self.send_error(500, str(e))
            print(e)
            e.with_traceback()

    def send_object(self, status: int, obj={}):
        self.send_success(status, "application/json",
                          bytes(json.dumps(obj), "utf-8"))

    def send_success(self, status: int, content_type="text/html", content=b''):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(content)


    def route(self):
        path, query = self.path.split("?") if self.path.__contains__('?')  else [self.path, ""]
        
        if path == "/":
            method_name =f"api_{self.command}_root"
        else:
            method_name =f"api_{self.command}{path.lower().replace('/', '_')}"

        if method_name in dir(self):
            getattr(self, method_name)()
        else :
            self.send_error(404, "Not Found", f"{path} was not found")


    def api_GET_root(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(
            bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def api_POST_root(self):
        length = int(self.headers['Content-Length'])
        content = str(self.rfile.read(length), encoding="utf-8")

        obj = {
            "hello": "meh",
            "cmd": self.command,
            "path": self.path,
            "content": content
        }
        self.send_object(202, obj)


    # /test
    def api_POST_test(self):
        self.send_object(200, {"hello": "meh"})
        pass

    def api_GET_test(self):
        self.send_object(200, {"YAY": "nice"})
        pass

    def api_GET_math(self):
        import math
        self.send_object(200, {
            'e': math.e,
            'pi': math.pi,
            'tau': math.tau,
        })
        pass


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
