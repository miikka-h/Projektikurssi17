#!/bin/python3

import sys
from queue import Queue, Empty
from threading import Thread, Event
import socket
import time

import evdev

from web_server import WebServer
from evdev import ecodes
from hid_report import HidReport
from device_finder import FindDevices

input_devices = []

def main():

    try:

        # if len(sys.argv) < 2:
        #    print("give evdev device file path as argument")
        #    exit(-1)

        device = Devices()
        
        # Firts we load all necessary components and form connections.

        server = Server()

        # hid data will be sent here. defined in the try block.
        socket_out = None

        try:
            socket_out = Socket_out()
        except OSError as error:
            print("error: " + error.strerror)
            server.close()
            socket_out.close()
            exit(-1)

        print("waiting for client")

        socket_out.findConnection()
        print("client from " + str(socket_out.address) + " connected")

        # Create evdev keycode to USB HID report converter.
        hid_report = HidReport()


        # Actual server logic loop.
        run(server, socket_out, hid_report)

    except KeyboardInterrupt:
        # handle ctrl-c
        server.close()
        socket_out.close()
        input_device.close()
        exit(0)


def run(server, socket_out, hid_report):

    clear_keys = True

    while True:

        #
        #Initialize input event reading.
        #input_device = evdev.InputDevice(sys.argv[1])
        #print(input_device)
        #
        #
        

        
        try:
            new_settings = server.settings_queue.get(block=False)
            print(str(new_settings))
        except Empty:
            pass

        key_update = False

        while True:
            event = input_device.read_one()

            if event is None:
                clear_keys = False
                break

            # add keys that are currently pressed down to the hid report.
            if event.type == ecodes.EV_KEY and not clear_keys:
                key_event = evdev.categorize(event)

                if key_event.keystate == key_event.key_down:
                    hid_report.add_key(key_event.scancode)
                    key_update = True
                elif key_event.keystate == key_event.key_up:
                    hid_report.remove_key(key_event.scancode)
                    key_update = True

            if key_update:
                hid_report.update_report()

                try:
                    socket_out.connection_socket.sendall(hid_report.report)
                except OSError as error:
                    print("error: " + error.strerror)
                    print("disconnecting client from: " + str(server.address))
                    socket_out.connection_socket.close()
                    print("waiting for new client")
                    (connection_socket, address) = server_socket.accept()
                    print("client from " + str(address) + " connected")
                    clear_keys = True

            time.sleep(0.01)


class Devices():

    def __init__(self):
        device_queue = Queue()
        self.exit_event = Event()
        self.device_search_thread = Thread(group=None, target=FindDevices, args=(device_queue, exit_event))
        self.device_search_thread.start()

    def close(self):
        self.exit_event.set()
        self.device_search_thread.join()
        

class Socket_out():

    def __init__(self):
        self.connection_socket = None
        self.address = None
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("", 25001))
        self.server_socket.listen(0)

    def close(self):
        self.server_socket.close()

    def findConnection(self):
        (self.connection_socket, self.address) = self.server_socket.accept()


class Server():

    def __init__(self):
        self.exit_event = Event()
        web_server_settings = ("", 8080)
        self.settings_queue = Queue()
        self.web_server_thread = Thread(group=None, target=WebServer, args=(web_server_settings, self.settings_queue, self.exit_event))
        self.web_server_thread.start()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close(self):
        self.exit_event.set()
        self.web_server_thread.join()


if __name__ == "__main__":
    main()
    print("main thread exitted")
