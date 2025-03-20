from http.server import HTTPServer, BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Handling POST requests
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello World")


# Starting server on port 8000
server = HTTPServer(("localhost", 8000), RequestHandler)
server.serve_forever()
