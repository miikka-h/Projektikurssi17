#!/bin/python3

import sys
from queue import Queue, Empty
from threading import Thread, Event
import socket
import time

import evdev

from web_server import WebServer
from evdev import KeyEvent, ecodes
from hid_report import HidReport

def main():

    # Check argument count.

    if len(sys.argv) < 2:
        print("give evdev device file path as argument")
        exit(-1)

    # Start web server.

    exit_event = Event()

    web_server_settings = ("", 8080)
    settings_queue = Queue()

    web_server_thread = Thread(group=None, target=WebServer, args=(web_server_settings, settings_queue, exit_event))
    web_server_thread.start()

    # Initialize input event reading.

    input_device = evdev.InputDevice(sys.argv[1])
    print(input_device)

    # Create evdev keycode to USB HID report converter.

    hid_report = HidReport()

    # Socket where USB HID data will be sent.

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("", 25001))
        server_socket.listen(0)
    except OSError as error:
        print("error: " + error.strerror)
        exit_event.set()
        web_server_thread.join()
        server_socket.close()
        input_device.close()
        exit(-1)

    # Wait client to connect.

    print("waiting for client")

    (connection_socket, address) = (None, None)

    try:
        (connection_socket, address) = server_socket.accept()
    except KeyboardInterrupt:
        # handle ctrl-c
        exit_event.set()
        web_server_thread.join()
        server_socket.close()
        input_device.close()
        exit(0)

    print("client from " + str(address) + " connected")

    # Server main loop.

    clear_keys = True

    try:
        while True:
            try:
                new_settings = settings_queue.get(block=False)
                print(str(new_settings))
            except Empty:
                pass

            key_update = False

            while True:
                event = input_device.read_one()

                if event is None:
                    clear_keys = False
                    break

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
                    connection_socket.sendall(hid_report.report)
                except OSError as error:
                    print("error: " + error.strerror)
                    print("disconnecting client from: " + str(address))
                    connection_socket.close()
                    print("waiting for new client")
                    (connection_socket, address) = server_socket.accept()
                    print("client from " + str(address) + " connected")
                    clear_keys = True

            time.sleep(0.01)

    except KeyboardInterrupt:
        # handle ctrl-c
        exit_event.set()
        web_server_thread.join()
        connection_socket.close()
        server_socket.close()
        input_device.close()



if __name__ == "__main__":
    main()
    print("main thread exitted")
