from http.server import HTTPServer, BaseHTTPRequestHandler
from queue import Queue, Empty
from threading import Thread, Event
import json
import os
import copy

# Import Tuple type which is used in optional function type annotations.
from typing import Tuple

import keyprofile


class WebServerManager():

    """Creates new web server thread."""

    def __init__(self):
        self.exit_event = Event()
        web_server_settings = ("", 8080)
        self.settings_queue = Queue()
        self.heatmap_queue = Queue()
        self.current_profile_queue = Queue()
        self.web_server_thread = Thread(group=None, target=WebServer, args=(
            web_server_settings, self.settings_queue, self.heatmap_queue, self.current_profile_queue, self.exit_event))
        self.web_server_thread.start()

    def close(self):
        """Close web server. This method will block until web server is closed."""
        self.exit_event.set()
        self.web_server_thread.join()

    def get_settings_queue(self) -> Queue:
        return self.settings_queue

    def get_heatmap_queue(self) -> Queue:
        return self.heatmap_queue

    def get_profile_queue(self) -> Queue:
        return self.current_profile_queue


class Heatmap:
    def __init__(self):
        self.heatmap_data = {}
        self.tempHeatmap_data = {}

    def add_keypress(self, evdev_id: int) -> None:
        key = str(evdev_id)

        try:
            self.heatmap_data[key] = self.heatmap_data[key] + 1
        except KeyError:
            self.heatmap_data[key] = 1

        try:
            self.tempHeatmap_data[key] = self.tempHeatmap_data[key] + 1
        except KeyError:
            self.tempHeatmap_data[key] = 1
            

    def get_heatmap_data(self):
        return self.heatmap_data

    def json_string(self) -> str:
        return json.dumps(self.heatmap_data)

    def set_heatmap_data(self, heatmap_data) -> None:
        self.heatmap_data = heatmap_data

    def get_tempHeatmap_data(self):
        return self.tempHeatmap_data

    def json_tempString(self) -> str:
        return json.dumps(self.tempHeatmap_data)

    def set_tempHeatmap_data(self, tempHeatmap_data) -> None:
        self.tempHeatmap_data = tempHeatmap_data


    def reset_tempHeatmap_data(self) -> None:
        self.tempHeatmap_data = {}


HEATMAP_FILE_NAME = 'heatmap_stats.txt'
#TEMPHEATMAT_FILE_NAME = 'temp_heatmap_stats.txt'
PROFILE_DATA_FILE_NAME = 'data.txt'
CURRENT_PROFILE_FILE_NAME = 'curprofile.txt'


# Class WebServer inherits HTTPServer class which is from Python standard library.
# https://docs.python.org/3/library/http.server.html

# Also, note that HTTPServer inherits TCPServer.
# https://docs.python.org/3/library/socketserver.html#socketserver.TCPServer
class WebServer(HTTPServer):

    # Type annotations of this constructor are optional.

    def __init__(self, address_and_port: Tuple[str, int], settings_queue: Queue, heatmap_queue: Queue, current_profile_queue: Queue, exit_event: Event) -> None:

        # Run constructor from HTTPServer first. Note the RequestHandler class.
        super().__init__(address_and_port, RequestHandler)

        # Some object attributes specific to this class. You can modify
        # them from RequestHandler's methods.
        self.settings_queue = settings_queue

        self.current_profile_queue = current_profile_queue

        # Check exit event every 0.5 seconds if there is no new TCP
        # connections.
        self.timeout = 0.5

        # Initialize profiles

        self.settings = [{}]
        
        if os.path.exists(PROFILE_DATA_FILE_NAME):
            with open(PROFILE_DATA_FILE_NAME, 'r') as profiles_file:
                file_contents = profiles_file.read()
                self.settings = json.loads(file_contents)

        self.current_profile = 1
        if os.path.exists(CURRENT_PROFILE_FILE_NAME):
            with open(CURRENT_PROFILE_FILE_NAME, 'r') as curprofile_file:
                file_contents = curprofile_file.read()
                self.current_profile = json.loads(file_contents)

        # Initialize heatmap

        self.heatmap = Heatmap()

        if os.path.exists(HEATMAP_FILE_NAME):
            with open(HEATMAP_FILE_NAME, 'r') as heatmap_file:
                file_contents = heatmap_file.read()
                heatmap_data = json.loads(file_contents)
                self.heatmap.set_heatmap_data(heatmap_data)

        # Main thread is waiting for profiles/settings so lets send them.
        parse_mappedEvdevID_and_send_settings(
            self.settings, self.settings_queue)

        set_current_profile(self.current_profile, self.current_profile_queue)

        print("web server running")
        while True:
            # This method will timeout because exit_event must be checked enough often
            # to shutdown cleanly.
            self.handle_request()

            if exit_event.is_set():
                # There was exit event, lets close the web server.
                break

            try:
                while True:
                    evdev_id = heatmap_queue.get(block=False)
                    self.heatmap.add_keypress(evdev_id)
                    
            except Empty:
                pass

            try:
                while True:
                    self.current_profile = current_profile_queue.get(block=False)
                    print("kissa istuu puussa " + str(self.current_profile))                    
            except Empty:
                pass    

        self.server_close()

        # Save profiles/settings.
        with open(PROFILE_DATA_FILE_NAME, 'w') as outfile:
            json.dump(self.settings, outfile)

        # Save heatmap.
        with open(HEATMAP_FILE_NAME, 'w') as outfile:
            outfile.write(self.heatmap.json_string())

        # Save information about current profile.
        with open(CURRENT_PROFILE_FILE_NAME, 'w') as outfile:
            json.dump(self.current_profile, outfile)


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

        # get key-binding settings in json form
        if self.path == "/json.api":
            message = json.dumps(self.server.settings)
            message_bytes = message.encode()

            self.send_utf8_bytes(message_bytes, "text/json")
        # get heatmap statistics in json form
        elif self.path == "/heatmap.api":
            text = self.server.heatmap.json_string()
            message_bytes = text.encode()
            self.send_utf8_bytes(message_bytes, "text/json")
        elif self.path == "/resetHeatmap.api":
            self.server.heatmap.reset_tempHeatmap_data()
            text = self.server.heatmap.json_tempString()
            message_bytes = text.encode()
            self.send_utf8_bytes(message_bytes, "text/json")
        elif self.path == "/tempHeatmap.api":
            text = self.server.heatmap.json_tempString()
            message_bytes = text.encode()
            self.send_utf8_bytes(message_bytes, "text/json")
        elif self.path == "/curprofile.api":
            text = str(self.server.current_profile)
            message_bytes = text.encode()
            self.send_utf8_bytes(message_bytes, "text/json")
        elif self.path == "/":
            self.send_utf8_file("../frontend/control.html", "text/html")
        elif self.path == "/webgl-keyboard":
            self.send_utf8_file(
                "../webgl-keyboard/dist/index.html", "text/html")
        elif self.path == "/styles.css":
            self.send_utf8_file("../frontend/styles.css", "text/css")
        elif self.path == "/script.js":
            self.send_utf8_file("../frontend/script.js",
                                "application/javascript")
        elif self.path == "/bundle.js":
            self.send_utf8_file(
                "../webgl-keyboard/dist/bundle.js", "application/javascript")
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

        parse_mappedEvdevID_and_send_settings(
            self.server.settings, self.server.settings_queue)
        print("abcdefghijklmn")

#        # prepare the loaded settings data for usage with hid data.
#
#        print(self.server.settings)
#        for profile in self.server.settings:
#            # try:
#            for key in profile["keyData"]:
#                list_of_hid_reports = []  # type: List[List[int]]
#                single_hid = []  # type: List[int]
#                if "mappedEvdevID" in profile["keyData"][key]:
#                    key_reports_strings = profile["keyData"][key][
#                        "mappedEvdevID"].split("|")
#                    for i in key_reports_strings:
#                        single_hid = [int(x) for x in i.split(":")]
#                        list_of_hid_reports.append(single_hid)
#                    profile["keyData"][key]["mappedEvdevID"] = list_of_hid_reports
#            # if "profile" in key:
#            # except KeyError as error:
#        print(self.server.settings)
#
#        # Send new settings to main thread.
#        self.server.settings_queue.put_nowait(self.server.settings)

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


def set_current_profile(current_profile, current_profile_queue):
    current_profile_queue.put_nowait(current_profile)

def parse_mappedEvdevID_and_send_settings(profile_list, settings_queue):
    """
    Parse key "mappedEvdevID" value "1:2:3|4:5:6" to
    [[1,2,3], [4,5,6]]
    """

    # Server must have original settings because it saves
    # the settings to a file, so lets make a copy
    new_settings = copy.deepcopy(profile_list)

    for profile in new_settings:
        if "keyData" not in profile:
            continue

        for evdev_id_key in profile["keyData"]:
            key_object = profile["keyData"][evdev_id_key]

            if "mappedEvdevID" not in key_object:
                continue

            hid_report_list = []

            hid_report_list_string = key_object["mappedEvdevID"]

            if hid_report_list_string == "undefined":
                key_object["mappedEvdevID"] = hid_report_list
                continue

            delay_list = []
            for key_string in hid_report_list_string.split("|"):

                if key_string[:1] == "$":
                    if len(key_string) > 1:
                        delay_number_string = key_string[1:]
                        delay_number = float(delay_number_string)
                        delay_list.pop()
                        delay_list.append(delay_number)
                    continue

                evdev_id_list = [int(x) for x in key_string.split(":")]
                hid_report_list.append(evdev_id_list)

                delay_list.append(0.1)

            key_object["mappedEvdevID"] = hid_report_list
            key_object["delay_list"] = delay_list

    # Send new settings to main thread.
    settings_queue.put_nowait(new_settings)
    
