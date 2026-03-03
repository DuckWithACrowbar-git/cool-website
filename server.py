import http.server
import socketserver
import ssl
import threading


# -----------------------------
# HTTP → HTTPS redirect server
# -----------------------------
class RedirectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        host = self.headers.get("Host", "").split(":")[0]
        new_url = f"https://{host}{self.path}"
        self.send_response(301)
        self.send_header("Location", new_url)
        self.end_headers()

    def log_message(self, *args):
        pass


def run_redirect():
    with socketserver.TCPServer(("", 80), RedirectHandler) as httpd:
        print("Redirecting all HTTP (80) → HTTPS (443)")
        httpd.serve_forever()


# -----------------------------
# HTTPS server
# -----------------------------
class SecureHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def run_https():
    httpd = socketserver.TCPServer(("", 443), SecureHandler)

    # Modern SSL setup
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print("Serving HTTPS on port 443")
    httpd.serve_forever()


# -----------------------------
# Run both servers
# -----------------------------
if __name__ == "__main__":
    threading.Thread(target=run_redirect, daemon=True).start()
    run_https()
