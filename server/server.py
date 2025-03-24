from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Handling POST requests

        use_float = False

        expression = "12+3"

        args = ["../build/app.exe"]
        if use_float:
            args.append("--float")

        res = subprocess.run(
            args,
            input=expression,
            text=True,
            capture_output=True
        )

        ans = res.stdout
        print(ans)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(ans.encode())


# Starting server on port 8000
server = HTTPServer(("localhost", 8000), RequestHandler)
server.serve_forever()
