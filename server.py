import http.server
import ssl
import socketserver
import threading


# -----------------------------
# 1. HTTP → HTTPS Redirect
# -----------------------------
class RedirectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        host = self.headers.get("Host", "")
        # Remove port if present
        host = host.split(":")[0]
        new_url = f"https://{host}{self.path}"
        self.send_response(301)
        self.send_header("Location", new_url)
        self.end_headers()

    def log_message(self, format, *args):
        return  # silence logs if desired


def run_redirect_server():
    with socketserver.TCPServer(("", 80), RedirectHandler) as httpd:
        print("HTTP redirect server running on port 80 → 443")
        httpd.serve_forever()


# -----------------------------
# 2. HTTPS Server
# -----------------------------
class SecureHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return  # silence logs if desired


def run_https_server():
    httpd = socketserver.TCPServer(("", 443), SecureHandler)

    # Load cert + key from same folder
    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        certfile="cert.pem",
        keyfile="key.pem",
        server_side=True
    )

    print("HTTPS server running on port 443")
    httpd.serve_forever()


# -----------------------------
# 3. Run both servers
# -----------------------------
if __name__ == "__main__":
    # Thread for HTTP redirect
    t = threading.Thread(target=run_redirect_server, daemon=True)
    t.start()

    # Main thread runs HTTPS
    run_https_server()
