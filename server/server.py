from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
from urllib.parse import urlparse, parse_qs


class CalculatorHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Handling POST requests
        parsed_url = urlparse(self.path)
        if parsed_url.path != "/calc":
            self.send_error(404, "Not Found")
            return

        query_params = parse_qs(parsed_url.query)
        use_float = query_params.get("float", ["float"])[0] == "true"
        print(use_float)

        content_length = int(self.headers.get("Content-Length"))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        expression = data.get("expression")
        print(expression)

        args = ["../build/app.exe"]
        if use_float:
            args.append("--float")

        res = subprocess.run(
            args,
            input=expression,
            text=True,
            capture_output=True
        )

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        
        response = {"result": res.stdout}
        self.wfile.write(json.dumps(response).encode())


# Starting server on port 8000
server = HTTPServer(("localhost", 8000), CalculatorHandler)
server.serve_forever()
