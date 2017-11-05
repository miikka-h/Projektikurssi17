#!/bin/python3

from queue import Queue, Empty
from threading import Thread, Event
import socket
import time
import keyprofile

import pyudev
import evdev

from web_server import WebServer
from evdev import ecodes
from hid_report import HidReport


def initkeyboards():
    device_list = []
    event_location = ""
    devinput = "/dev/input/"
    context = pyudev.Context()
    for device in context.list_devices():
        if 'ID_INPUT_KEYBOARD' in device:
            try:
                event_location = device.device_node
                if event_location[0:(len(devinput))] == devinput:
                    device_list.append(evdev.InputDevice(event_location))
            except TypeError:
                pass

    return device_list


device_list = initkeyboards()


def log_event(action, device):
    event_location = ""
    devinput = "/dev/input/"
    if 'ID_INPUT_KEYBOARD' in device:
        try:
            event_location = device.device_node
            print('{0} - {1}'.format(action, event_location))
            if event_location[0:(len(devinput))] == devinput:
                if action == "add":
                    device_list.append(evdev.InputDevice(event_location))
                else:
                    try:
                        device_list.remove(event_location)
                    except ValueError:
                        pass
                print(device_list)
        except TypeError:
            pass
# keyboard detection


def main():

    try:

        # initialize all connected keyboards
        # initKeyboards()

        # Starts looking for new connected keyboards
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by('input')

        print("Waiting for keyboards to be connected")
        observer = pyudev.MonitorObserver(monitor, log_event)
        observer.start()

        # Lets load all necessary components and form connections.

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
        exit(0)


def run(server, socket_out, hid_report):

    clear_keys = True

    new_settings = keyprofile.settings

    while True:

        if len(device_list) < 1:
            time.sleep(0.1)
            continue

        try:
            new_settings = server.settings_queue.get(block=False)
            print(str(new_settings))
        except Empty:
            pass

        for input_device in device_list:
            key_update = False
            print(input_device)

            while True:
                event = input_device.read_one()

                if event is None:
                    clear_keys = False
                    break

                # add keys that are currently pressed down to the hid report.
                if event.type == ecodes.EV_KEY and not clear_keys:
                    key_event = evdev.categorize(event)

                    mappedIDs = []
                    for key in new_settings["keyData"]:
                        if key["EvdevID"] == key_event.scancode:
                            if isinstance(key["mappedEvdevID"], str):
                                mappedIDs = [int(x) for x in key["mappedEvdevID"].split(" ")]
                            else:
                                mappedIDs.append(key["mappedEvdevID"])
                            break

                    if key_event.keystate == key_event.key_down:
                        for k in mappedIDs:
                            if hid_report.add_key(k):
                                key_update = True

                    elif key_event.keystate == key_event.key_up:
                        for k in mappedIDs:
                            if hid_report.remove_key(k):
                                key_update = True

                    if key_update:
                        hid_report.update_report()

                        try:
                            socket_out.connection_socket.sendall(hid_report.report)
                        except OSError as error:
                            print("error: " + error.strerror)
                            print("disconnecting client from: " + str(server.address))
                            socket_out.connection_socket.close()
                            clear_keys = True

            time.sleep(0.01)


# class Devices():
# 
#     def __init__(self):
#         device_queue = Queue()
#         self.exit_event = Event()
#         self.device_search_thread = Thread(group=None, target=FindDevices, args=(device_queue, exit_event))
#         self.device_search_thread.start()
# 
#     def close(self):
#         self.exit_event.set()
#         self.device_search_thread.join()


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
