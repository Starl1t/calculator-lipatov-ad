from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import subprocess
from urllib.parse import urlparse, parse_qs
import structlog
import logging


def setup_logging():
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.processors.JSONRenderer()
    )

    console_formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.dev.ConsoleRenderer()
    )

    file_handler = logging.FileHandler("app.log", mode="w")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)

    root_logger.handlers.clear()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


class CalculatorHandler(BaseHTTPRequestHandler):
    def _parse_request_url(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path != "/calc":
            self.send_error(404, "Not Found")
            return False
        else:
            logger.info("Parsing url", path=parsed_url.path)
            return parsed_url

    def _get_query_params(self, parsed_url):
        query_params = parse_qs(parsed_url.query)
        use_float = query_params.get("float", ["float"])[0] == "true"
        logger.info("Getting query parameters", float=use_float)

        return use_float

    def _get_post_data(self):
        content_length = int(self.headers.get("Content-Length"))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        expression = data.get("expression")
        logger.info("Getting post data", data=expression)

        return expression

    def _execute_calculation(self, expression, use_float):
        args = ['build/app.exe']
        if use_float:
            args.append("--float")

        res = subprocess.run(
            args,
            input=expression,
            text=True,
            capture_output=True
        )

        logger.info("Executing calculation",
                    expression=expression, result=res.stdout)

        return res

    def _send_post_response(self, calculation_result):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        response = {"result": calculation_result.stdout}
        self.wfile.write(json.dumps(response).encode())

        logger.info("Sending response", response=response)

    def do_POST(self):
        parsed_url = self._parse_request_url()
        if not parsed_url:
            return

        use_float = self._get_query_params(parsed_url)
        expression = self._get_post_data()

        res = self._execute_calculation(expression, use_float)

        self._send_post_response(res)


def start_server():
    server = HTTPServer(("localhost", 8000), CalculatorHandler)
    logger.info("Starting server")
    server.serve_forever()


if __name__ == "__main__":
    setup_logging()
    logger = structlog.get_logger()
    start_server()
