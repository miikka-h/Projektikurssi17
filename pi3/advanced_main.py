#!/bin/python3

from queue import Queue, Empty
from threading import Thread, Event
import socket
import time
from typing import List

import pyudev
import evdev
from evdev import ecodes

from web_server import WebServerManager
from hid_report import HidReport

class HidDataSocket():

    def __init__(self) -> None:
        self.server_socket = None # type: socket.SocketType
        self.connection_socket = None # type: socket.SocketType
        self.address = None

    # Return False if there is socket creation error.
    def create_socket(self) -> bool:
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("", 25001))
            self.server_socket.listen(0)
            return True
        except OSError as error:
            print("error: " + error.strerror)
            return False

    def close(self) -> None:
        if self.connection_socket is not None:
            self.connection_socket.close()

            self.server_socket.close()

    def wait_connection(self) -> None:
        if self.connection_socket is not None:
            self.connection_socket.close()

        print("waiting for client")
        (self.connection_socket, self.address) = self.server_socket.accept()
        print("client from " + str(self.address) + " connected")

    # Returns False if client disconnected.
    def send_hid_report(self, hid_report: HidReport) -> bool:
        hid_report.update_report()

        try:
            self.connection_socket.sendall(hid_report.report)
            return True
        except OSError as error:
            print("error: " + error.strerror)
            print("client " + str(self.address) + "disconnected")
            return False


class KeyRemapper:
    def __init__(self, settings) -> None:
        self.settings = settings

    def set_new_settings(self, settings) -> None:
        self.settings = settings

    def remap_key(self, evdev_id: int) -> List[List[int]]:
        key_reports = [] # type: List[List[int]]

        mapped_ids = [] # type: List[int]

        # TODO: Remove for loop. That requires changes in JSON structure.
        for key in self.settings["keyData"]:
            if key["EvdevID"] == evdev_id:
                if isinstance(key["mappedEvdevID"], str):
                    mapped_ids = [int(x) for x in key["mappedEvdevID"].split(" ")]
                else:
                    mapped_ids.append(key["mappedEvdevID"])
                key_reports.append(mapped_ids)
                break

        return key_reports



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
            print (device_list)
            event_location = device.device_node
            print('{0} - {1}'.format(action, event_location))
            if event_location[0:(len(devinput))] == devinput:
                if action == "add":
                    device_list.append(evdev.InputDevice(event_location))
                else:
                    print("removing" + event_location)
                    for i in device_list:
                        try:
                            print(i.device_node)
                        except AttributeError:
                            print("actual removal happening")
                            device_list.remove(i)


                   # i = len (device_list) -1
                   # while i >= 0:
                   #     try:
                   #         if device
                   #     except FileNotFoundError:
                   #         del device_list[i]
                   #     i -= 1
                   # try:
                   #     device_list.remove(evdev.InputDevice(event_location))
                   # except ValueError:
                   #     pass
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

        web_server_manager = WebServerManager()

        hid_data_socket = HidDataSocket()

        if not hid_data_socket.create_socket():
            print("error: Could not create socket for HidDataSocket.")
            web_server_manager.close()
            hid_data_socket.close()
            exit(-1)

        hid_data_socket.wait_connection()

        # Create evdev keycode to USB HID report converter.
        hid_report = HidReport()

        # Actual server logic loop.
        run(web_server_manager, hid_data_socket, hid_report)

    except KeyboardInterrupt:
        # handle ctrl-c
        web_server_manager.close()
        hid_data_socket.close()
        exit(0)


def run(web_server_manager: WebServerManager, hid_data_socket: HidDataSocket, hid_report: HidReport) -> None:

    clear_keys = True

    print("waiting for settings from web server thread")
    key_remapper = KeyRemapper(web_server_manager.get_settings_queue().get())
    print("received settings from web server thread")

    while True:

        if len(device_list) < 1:
            time.sleep(0.1)
            continue

        try:
            new_settings = web_server_manager.get_settings_queue().get(block=False)
            key_remapper.set_new_settings(new_settings)
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

                if event.type == ecodes.EV_KEY and not clear_keys:

                    new_keys_list = key_remapper.remap_key(event.code)

                    if len(new_keys_list) == 1:
                        key_list = new_keys_list[0]

                        # key_down = 1
                        if event.value == 1:
                            for k in key_list:
                                if hid_report.add_key(k):
                                    key_update = True
                        # key_up = 0
                        elif event.value == 0:
                            for k in key_list:
                                if hid_report.remove_key(k):
                                    key_update = True
                    else:
                        pass
                        # TODO: Handle more complicated key remaps.

                    if key_update:
                        if not hid_data_socket.send_hid_report(hid_report):
                            hid_data_socket.wait_connection()
                            clear_keys = True

            time.sleep(0.1)


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



if __name__ == "__main__":
    main()
    print("main thread exitted")
