import http.server 
import socketserver 

class RedirectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self)
        self.send_response(301)
        new_url = f"https://{self.headers['Host'].split(':'[0]}{self.path}"
        self.send_header("Location", new_url)
        self.end_headers()

with socketserver.TCPServer(("", 80), RedirectHandler) as httpd:
    print("Redirection is up and working")
    httpd.serve_forever()
