

from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from queue import Queue
from threading import Event


from typing import Tuple


class WebServer(HTTPServer):
    def __init__(self, address_and_port: Tuple [str, int], settings_queue: Queue, exit_event: Event) -> None:
        super().__init__(address_and_port, RequestHandler)
        self.settings_queue = settings_queue
        self.settings = {
            "profile_name": "TODO: real settings"
        }

        # Check exit event every 0.5 seconds if there is no new TCP connections.
        self.timeout = 0.5

        print("web server running")
        while True:
            self.handle_request()

            if exit_event.is_set():
                break

        self.server_close()
        print("web server exited")


class RequestHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self) -> None:
        print("GET")
        print("path: " + self.path)
        print("client_address: " + str(self.client_address))
        print("request_version: " + self.request_version)
        print("headers: " + str(self.headers))

        message_bytes = b"<html><body><h1>Hello world</h1></body></html>"

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Length", str(len(message_bytes)))
        self.send_header("Content-Encoding", "UTF-8")
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        self.wfile.write(message_bytes)
        self.wfile.flush()
        print("response sent")

    def do_POST(self) -> None:
        print("POST")
        print("path: " + self.path)
        print("client_address: " + str(self.client_address))
        print("request_version: " + self.request_version)
        print("headers: " + str(self.headers))

        # Send new settings to main thread.
        self.server.settings_queue.put_nowait(self.server.settings)

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Length", "0")
        self.end_headers()
        print("response sent")

