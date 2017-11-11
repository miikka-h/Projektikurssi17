from http.server import HTTPServer, BaseHTTPRequestHandler
from queue import Queue
from threading import Event
import keyprofile
import json
import codecs

# Import Tuple type which is used in optional function type annotations.
from typing import Tuple

# Class WebServer inherits HTTPServer class which is from Python standard library.
# https://docs.python.org/3/library/http.server.html

# Also, note that HTTPServer inherits TCPServer.
# https://docs.python.org/3/library/socketserver.html#socketserver.TCPServer
class WebServer(HTTPServer):
    # Type annotations of this constructor are optional.
    def __init__(self, address_and_port: Tuple [str, int], settings_queue: Queue, exit_event: Event) -> None:
        # Run constructor from HTTPServer first. Note the RequestHandler class.
        super().__init__(address_and_port, RequestHandler)

        # Some object attributes specific to this class. You can modify
        # them from RequestHandler's methods.
        self.settings_queue = settings_queue
        self.settings = keyprofile.settings

        # Check exit event every 0.5 seconds if there is no new TCP connections.
        self.timeout = 0.5

        print("web server running")
        while True:
            # This method will timeout because exit_event must be checked enough often
            # to shutdown cleanly.
            self.handle_request()

            if exit_event.is_set():
                # There was exit event, lets close the web server.
                break

        self.server_close()
        print("web server exited")


# Python standard library HTTPServer works with request handler system, so lets
# make our own request handler.
class RequestHandler(BaseHTTPRequestHandler):
    # By default the HTTP version would be 1.0, so lets override it.
    # Note that HTTP 1.1 will use single TCP connection for every HTTP
    # request, so Content-Length header must be set for every HTTP response.
    # Otherwise web browser does not know when TCP connection should be closed.
    #protocol_version = "HTTP/1.1"

    # Handler for HTTP GET requests.
    def do_GET(self) -> None:
        # Print some information about the HTTP request.
        print("GET")
        print("path: " + self.path) 
        print("client_address: " + str(self.client_address))
        print("request_version: " + self.request_version)
        print("headers: " + str(self.headers))
        

        
        
        if self.path == "/json.api":
            message = json.dumps(self.server.settings)
            message_bytearray = bytearray()
            message_bytearray.extend(map(ord, message))
             # 200 is HTTP status code for successfull request.
            self.send_response(200)
            # Content-Length is length of the HTTP message body in bytes.
            self.send_header("Content-Length", str(len(message_bytearray)))
            self.send_header("Content-Encoding", "UTF-8")
            self.send_header("Content-Type", "text/json; charset=utf-8")
            self.end_headers()
            # Write HTTP message body which is the HTML web page.
            self.wfile.write(message_bytearray)
            self.wfile.flush()
            print("response sent")
        elif self.path == "/":
            
            f = codecs.open("../frontend/control.html", 'r')
            message = f.read()
            f.close()
           
            message_bytearray = bytearray()
            message_bytearray.extend(map(ord, message))
             # 200 is HTTP status code for successfull request.
            self.send_response(200)
            # Content-Length is length of the HTTP message body in bytes.
            self.send_header("Content-Length", str(len(message_bytearray)))
            self.send_header("Content-Encoding", "UTF-8")
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            # Write HTTP message body which is the HTML web page.
            
            self.wfile.write(message_bytearray)
            self.wfile.flush()
            print("response sent")    
        elif self.path == "/styles.css":
            
            f = codecs.open("../frontend/styles.css", 'r')
            message = f.read()
            f.close()
           
            message_bytearray = bytearray()
            message_bytearray.extend(map(ord, message))
             # 200 is HTTP status code for successfull request.
            self.send_response(200)
            # Content-Length is length of the HTTP message body in bytes.
            self.send_header("Content-Length", str(len(message_bytearray)))
            self.send_header("Content-Encoding", "UTF-8")
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.end_headers()

            # Write HTTP message body which is the HTML web page.
            
            self.wfile.write(message_bytearray)
            self.wfile.flush()
            print("response sent")
        elif self.path == "/script.js":
            
            f = codecs.open("../frontend/script.js", 'r')
            message = f.read()
            f.close()
           
            message_bytearray = bytearray()
            message_bytearray.extend(map(ord, message))
             # 200 is HTTP status code for successfull request.
            self.send_response(200)
            # Content-Length is length of the HTTP message body in bytes.
            self.send_header("Content-Length", str(len(message_bytearray)))
            self.send_header("Content-Encoding", "UTF-8")
            self.send_header("Content-Type", "application/javascript; charset=utf-8")
            self.end_headers()

            # Write HTTP message body which is the HTML web page.
            
            self.wfile.write(message_bytearray)
            self.wfile.flush()
            print("response sent")                
        else:
            message_bytearray = b"<html><body><h1>Hello world</h1></body></html>"
            # 200 is HTTP status code for successfull request.
            self.send_response(200)
            # Content-Length is length of the HTTP message body in bytes.
            self.send_header("Content-Length", str(len(message_bytearray)))
            self.send_header("Content-Encoding", "UTF-8")
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            # Write HTTP message body which is the HTML web page.
            self.wfile.write(message_bytearray)
            self.wfile.flush()
            print("response sent")

    # Handler for HTTP POST requests.
    def do_POST(self) -> None:
        print("POST")
        print("path: " + self.path)
        headerLength =  self.headers.get("Content-Length",0)

        response = self.rfile.read(int(headerLength))
       
        keyprofile_data = json.loads(response.decode("utf-8"))
        modified_keys = []
        if len(keyprofile_data) > 1:
            modified_keys = keyprofile_data
        for k in self.server.settings["keyData"]:
            for j in modified_keys["keyData"]: 
                if k["EvdevID"] == j["EvdevID"]:
                    k["mappedEvdevID"] = j["mappedEvdevID"]   
                    k["mappedEvdevName"] = j["mappedEvdevName"]

        
        
        print("client_address: " + str(self.client_address))
        print("request_version: " + self.request_version)
        print("headers: " + str(self.headers))

        # Send new settings to main thread.
        self.server.settings_queue.put_nowait(self.server.settings)

        self.send_response(200)
        self.send_header("Content-Length", "0")
        self.end_headers()
        print("response sent")
        #print(self.server.settings)
        with open('data.txt', 'w') as outfile:
            json.dump(self.server.settings, outfile)


