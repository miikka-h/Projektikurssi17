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

input_devices = []

def main():

    try:

        if len(sys.argv) < 2:
            print("give evdev device file path as argument")
            exit(-1)

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


        socket_out.findConnection()

        # Initialize input event reading.
        input_device = evdev.InputDevice(sys.argv[1])
        print(input_device)

        # Create evdev keycode to USB HID report converter.
        hid_report = HidReport()


        # Actual server logic loop.
        run(server, socket_out, hid_report, input_device)

    except KeyboardInterrupt:
        # handle ctrl-c
        server.close()
        socket_out.close()
        input_device.close()
        exit(0)


def run(server, socket_out, hid_report, input_device):

    clear_keys = True

    while True:
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
                    print("disconnecting client from: " + str(socket_out.address))
                    socket_out.findConnection()
                    clear_keys = True

            time.sleep(0.01)


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
        if self.connection_socket is not None:
            self.connection_socket.close()

        print("waiting for client")
        (self.connection_socket, self.address) = self.server_socket.accept()
        print("client from " + str(self.address) + " connected")


class Server():

    def __init__(self):
        self.exit_event = Event()
        web_server_settings = ("", 8080)
        self.settings_queue = Queue()
        self.web_server_thread =Thread(group=None, target=WebServer, args=(web_server_settings, self.settings_queue, self.exit_event))
        self.web_server_thread.start()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close(self):
        self.exit_event.set()
        self.web_server_thread.join()


if __name__ == "__main__":
    main()
    print("main thread exitted")
