from http.server import HTTPServer, BaseHTTPRequestHandler
from queue import Queue
from threading import Thread, Event
import json

# Import Tuple type which is used in optional function type annotations.
from typing import Tuple

import keyprofile


class WebServerManager():

    """Creates new web server thread."""

    def __init__(self):
        self.exit_event = Event()
        web_server_settings = ("", 8080)
        self.settings_queue = Queue()
        self.web_server_thread = Thread(group=None, target=WebServer, args=(
            web_server_settings, self.settings_queue, self.exit_event))
        self.web_server_thread.start()

    def close(self):
        """Close web server. This method will block until web server is closed."""
        self.exit_event.set()
        self.web_server_thread.join()

    def get_settings_queue(self) -> Queue:
        return self.settings_queue


# Class WebServer inherits HTTPServer class which is from Python standard library.
# https://docs.python.org/3/library/http.server.html

# Also, note that HTTPServer inherits TCPServer.
# https://docs.python.org/3/library/socketserver.html#socketserver.TCPServer
class WebServer(HTTPServer):
    # Type annotations of this constructor are optional.

    def __init__(self, address_and_port: Tuple[str, int], settings_queue: Queue, exit_event: Event) -> None:
        # Run constructor from HTTPServer first. Note the RequestHandler class.
        super().__init__(address_and_port, RequestHandler)

        # Some object attributes specific to this class. You can modify
        # them from RequestHandler's methods.
        self.settings_queue = settings_queue

        # Check exit event every 0.5 seconds if there is no new TCP
        # connections.
        self.timeout = 0.5

        # TODO: Load saved profiles/settings from file
        #       if file is not found default to keyprofile.settings
        self.settings = [{}]
        # keyprofile.setting

        # Main thread is waiting for profiles/settings so lets send them.
        self.settings_queue.put_nowait(self.settings)

        print("web server running")
        while True:
            # This method will timeout because exit_event must be checked enough often
            # to shutdown cleanly.
            self.handle_request()

            if exit_event.is_set():
                # There was exit event, lets close the web server.
                break

        self.server_close()

        # Save profiles/settings.
        with open('data.txt', 'w') as outfile:
            json.dump(self.settings, outfile)

        print("web server exited")


# Python standard library HTTPServer works with request handler system, so lets
# make our own request handler.
class RequestHandler(BaseHTTPRequestHandler):
    # By default the HTTP version is 1.0.

    def do_GET(self) -> None:
        """Handler for HTTP GET requests."""
        # Print some information about the HTTP request.

        # print("HTTP GET Request, path: " + self.path)
        # print("client_address: " + str(self.client_address))
        # print("request_version: " + self.request_version)
        # print("headers: " + str(self.headers))

        if self.path == "/json.api":
            message = json.dumps(self.server.settings)
            message_bytes = message.encode()

            self.send_utf8_bytes(message_bytes, "text/json")
        elif self.path == "/":
            self.send_utf8_file("../frontend/control.html", "text/html")
        elif self.path == "/styles.css":
            self.send_utf8_file("../frontend/styles.css", "text/css")
        elif self.path == "/script.js":
            self.send_utf8_file(
                "../frontend/script.js", "application/javascript")
        else:
            message_bytes = b"<html><body><h1>Hello world</h1></body></html>"
            self.send_utf8_bytes(message_bytes, "text/html")

    def do_POST(self) -> None:
        """Handler for HTTP POST requests."""
        # print("HTTP POST Request, path: " + self.path)
        # print("client_address: " + str(self.client_address))
        # print("request_version: " + self.request_version)
        # print("headers: " + str(self.headers))

        content_length = self.headers.get("Content-Length", 0)

        response = self.rfile.read(int(content_length))

        self.server.settings = json.loads(response.decode("utf-8"))

        # prepare the loaded settings data for usage with hid data.
        list_of_hid_reports = []  # type: List[List[int]]
        single_hid = []  # type: List[int]
        for profile in self.server.settings:
            try:
                for key in profile["keyData"]:

                    if "mappedEvdevID" in key:
                            key_reports_strings = key[
                                "mappedEvdevID"].split("|")
                            for i in key_reports_strings:
                                single_hid = [int(x) for x in i.split(":")]
                                list_of_hid_reports.append(single_hid)
                                print(list_of_hid_reports)
                            key["mappedEvdevID"] = list_of_hid_reports

                            # if "profile" in key:

        # Send new settings to main thread.
        self.server.settings_queue.put_nowait(self.server.settings)

        self.send_response(200)
        self.end_headers()

    def send_utf8_file(self, file_name: str, mime_type: str) -> None:
        """Mime type is string like 'text/json'"""
        file = open(file_name, mode='rb')
        file_as_bytes = file.read()
        file.close()

        self.send_utf8_bytes(file_as_bytes, mime_type)

    def send_utf8_bytes(self, message_bytes: bytes, mime_type: str) -> None:
        """Mime type is string like 'text/json'"""
        # 200 is HTTP status code for successfull request.
        self.send_response(200)
        self.send_header("Content-Encoding", "UTF-8")
        self.send_header("Content-Type", mime_type + "; charset=utf-8")
        self.end_headers()
        # Write HTTP message body which is the HTML web page.
        self.wfile.write(message_bytes)
        self.wfile.flush()
