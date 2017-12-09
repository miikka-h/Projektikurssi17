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

    """
    TCP Socket for sending USB HID report data.

    Call `create_socket()` method before using other methods.
    """

    def __init__(self) -> None:
        self.server_socket = None  # type: socket.SocketType
        self.connection_socket = None  # type: socket.SocketType
        self.address = None

    def create_socket(self) -> bool:
        """Returns False if there is socket creation error."""
        try:
            self.server_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("", 25001))
            self.server_socket.listen(0)
            return True
        except OSError as error:
            print("error: " + error.strerror)
            return False

    def close(self) -> None:
        """Close all sockets."""
        if self.connection_socket is not None:
            self.connection_socket.close()

        if self.server_socket is not None:
            self.server_socket.close()

    def wait_connection(self) -> None:
        """Close previous connection to client if it exists and wait for new connection."""
        if self.connection_socket is not None:
            self.connection_socket.close()

        print("waiting for client")
        (self.connection_socket, self.address) = self.server_socket.accept()
        print("client from " + str(self.address) + " connected")

    def send_hid_report_if_there_is_new_changes(self, hid_report: HidReport) -> bool:
        """Returns False if client disconnected."""
        if not hid_report.update_report():
            return True

        try:
            self.connection_socket.sendall(hid_report.report)
            return True
        except OSError as error:
            print("error: " + error.strerror)
            print("client " + str(self.address) + " disconnected")
            return False


class KeyRemapper:

    """Map one key to multiple keys."""

    def __init__(self, settings) -> None:
        """Argument `settings` is profile JSON dictionary."""
        self.settings = settings

        if len(self.settings) == 0:
            self.current_profile = None
        else:
            self.current_profile = self.settings[0]

    def set_new_settings(self, settings) -> None:
        """Argument `settings` is profile JSON dictionary."""
        self.settings = settings

        if len(self.settings) == 0:
            self.current_profile = None
        else:
            self.current_profile = self.settings[0]

    def change_profile(self, evdev_id: int) -> bool:
        """"Returns True if profile changed"""

        if self.current_profile == None:
            return False

        try:
            profile_list = self.current_profile["keyData"][str(evdev_id)]["profiles"]

            if len(profile_list) == 0:
                return False

            # change to first profile in the list
            next_id = profile_list[0]

            (result, profile_index) = self.profile_id_to_index(next_id)
            if not result:
                print("profile id " + str(next_id) + " does not exists")
                return False

            self.current_profile = self.settings[profile_index]
            print("changed profile index to " + str(profile_index) + ", id: " + str(next_id))

            return True
        except KeyError:
            pass

        return False

    def profile_id_to_index(self, profile_id: int) -> (bool, int):
        """Returns (True, index) if profile id exists"""

        for i in range(0, len(self.settings)):
            profile = self.settings[i]
            if "profileID" not in profile:
                continue

            if profile["profileID"] == profile_id:
                return (True, i)

        return (False, 0)


    def remap_key(self, evdev_id: int) -> List[List[int]]:
        """
        Remaps one key to multiple keys.

        Key id values are evdev id numbers.

        Returns list containing lists of keys. List of keys
        represents keys that are included in one USB hid report.

        Key "mappedEvdevID" value is a list like
        [[1,2,3], [4,5,6]]

        """

        if self.current_profile == None:
            return [[evdev_id]]

        try:
            return self.current_profile["keyData"][str(evdev_id)]["mappedEvdevID"]
        except KeyError as error:
            pass

        return [[evdev_id]]


class KeyboardManager:

    """Read input from all availlable keyboards.

    Starts a new thread to monitor device events from Linux udev system.
    This allows adding and removing keyboards at runtime without constantly
    polling udev for new device events.

    Call `close()` to close device monitoring thread.
    """

    def __init__(self) -> None:
        self.context = pyudev.Context()
        self.device_list = []  # type: List[evdev.InputDevice]

        for keyboard in self.context.list_devices(subsystem="input", ID_INPUT_KEYBOARD=1):
            if keyboard.device_node != None:
                keyboard = evdev.InputDevice(keyboard.device_node)
                print("Keyboard '" + keyboard.name + "' added")
                try:
                    keyboard.grab()
                except IOError:
                    print("cant't grab keyboard " + keyboard.name)
                self.device_list.append(keyboard)

        monitor = pyudev.Monitor.from_netlink(self.context)
        monitor.filter_by("input")

        self.exit_event = Event()
        self.event_queue = Queue()  # type: Queue
        self.device_monitor_thread = Thread(
            group=None, target=monitor_device_events, args=(self.exit_event, self.event_queue, monitor))
        self.device_monitor_thread.start()

        self.key_event_buffer = []  # type: List[evdev.InputEvent]
        self.clear_keys = False

    def close(self) -> None:
        """Send exit event to device monitoring thread. Waits until thread is closed."""

        for keyboard in self.device_list:
            try:
                keyboard.ungrab()
            except IOError:
                pass

        self.exit_event.set()
        self.device_monitor_thread.join()

    def get_key_events(self) -> List[evdev.InputEvent]:
        """
        Returns list of evdev keyboard events from all currently connected keyboards.

        If clearing current key events is requested, returns empty list.
        """
        self.key_event_buffer.clear()

        for keyboard in self.device_list:
            while True:
                try:
                    evdev_event = keyboard.read_one()

                    if evdev_event is None:
                        break
                    elif evdev_event.type == ecodes.EV_KEY and not self.clear_keys:
                        self.key_event_buffer.append(evdev_event)
                except OSError:
                    break

        self.clear_keys = False

        return self.key_event_buffer

    def request_clear_key_events(self) -> None:
        """
        Request clearing key event buffers. Clearing key events will
        happen at next `get_key_events()` method call.
        """
        self.clear_keys = True

    def check_device_events(self) -> None:
        """
        Check if there new device events from device monitoring thread.
        Updates keyboard list if there is new events.
        """
        while True:
            try:
                (event, device_node) = self.event_queue.get(block=False)

                if event == KEYBOARD_ADDED:
                    keyboard = evdev.InputDevice(device_node)
                    print("Keyboard '" + keyboard.name + "' added")
                    self.device_list.append(keyboard)
                elif event == KEYBOARD_REMOVED:
                    removed_device = None

                    for evdev_device in self.device_list:
                        if evdev_device.fn == device_node:
                            removed_device = evdev_device
                            break

                    if removed_device != None:
                        print("Keyboard '" + removed_device.name + "' removed")
                        self.device_list.remove(removed_device)
                        removed_device.close()
            except Empty:
                break


KEYBOARD_ADDED = 0
KEYBOARD_REMOVED = 1


def monitor_device_events(exit_event: Event, event_queue: Queue, monitor: pyudev.Monitor):
    """
    A new thread should be created to run this function.
    """
    while True:
        device = monitor.poll(timeout=0.5)

        if device != None:
            if not ('ID_INPUT_KEYBOARD' in device.properties and device.device_node != None):
                continue

            if device.action == "add":
                event_queue.put_nowait((KEYBOARD_ADDED, device.device_node))
            elif device.action == "remove":
                event_queue.put_nowait((KEYBOARD_REMOVED, device.device_node))

        if exit_event.is_set():
            break


def main():

    try:
        # Lets load all necessary components and form connections.
        keyboard_manager = KeyboardManager()

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
        run(web_server_manager, hid_data_socket, hid_report, keyboard_manager)

    except KeyboardInterrupt:
        # handle ctrl-c
        web_server_manager.close()
        hid_data_socket.close()
        keyboard_manager.close()
        exit(0)


def run(web_server_manager: WebServerManager, hid_data_socket: HidDataSocket, hid_report: HidReport, keyboard_manager: KeyboardManager) -> None:


    print("waiting for settings from web server thread")
    key_remapper = KeyRemapper(web_server_manager.get_settings_queue().get())
    print("received settings from web server thread")

    keyboard_manager.request_clear_key_events()

    while True:
        time.sleep(0.001)

        keyboard_manager.check_device_events()

        try:
            new_settings = web_server_manager.get_settings_queue().get(
                block=False)
            key_remapper.set_new_settings(new_settings)
        except Empty:
            pass


        for event in keyboard_manager.get_key_events():
            if event.value == 1:
                web_server_manager.get_heatmap_queue().put_nowait(event.code)

                if key_remapper.change_profile(event.code):
                    continue

            new_keys_list = key_remapper.remap_key(event.code)

            if len(new_keys_list) == 1:
                key_list = new_keys_list[0]

                # key_down = 1
                if event.value == 1:
                    for k in key_list:
                        hid_report.add_key(k)
                    send_and_reset_if_client_disconnected(hid_data_socket, hid_report, keyboard_manager)

                # key_up = 0
                elif event.value == 0:
                    for k in key_list:
                        hid_report.remove_key(k)
                    send_and_reset_if_client_disconnected(hid_data_socket, hid_report, keyboard_manager)
            else:
                if event.value == 1:
                    for report in new_keys_list:
                        key_list = report

                        for k in key_list:
                            hid_report.add_key(k)

                        send_and_reset_if_client_disconnected(
                            hid_data_socket, hid_report, keyboard_manager)

                        for k in key_list:
                            hid_report.remove_key(k)

                        send_and_reset_if_client_disconnected(
                            hid_data_socket, hid_report, keyboard_manager)

                        time.sleep(0.1)

def send_and_reset_if_client_disconnected(hid_data_socket: HidDataSocket, hid_report: HidReport, keyboard_manager: KeyboardManager) -> None:
    if not hid_data_socket.send_hid_report_if_there_is_new_changes(hid_report):
        hid_data_socket.wait_connection()
        keyboard_manager.request_clear_key_events()
        hid_report.clear()


if __name__ == "__main__":
    main()
    print("main thread exitted")
