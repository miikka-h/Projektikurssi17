#!/bin/python3

from queue import Queue, Empty
from threading import Thread, Event
from collections import OrderedDict
import socket
import time
from typing import List
import sys

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

                if len(sys.argv) > 1 and sys.argv[1] == "--grab-keyboards":
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


def mapProfiles(settings):
    """Profile ID mapped to index in the list in an OrderedDict"""

    profileMap = OrderedDict()
    i = 0
    print(settings)
    while i < len(settings):
        if "profileID" in settings[i]:
            index = settings[i]["profileID"]
            profileMap[index] = i
        i = i + 1

    return profileMap


def cutfrom(key: int, elements: OrderedDict):
    """Expects that the key is in the elements list and
    remove all elements after and including that position."""

    while (key in elements):
        print(key)
        elements.popitem(last=True)


class KeyRemapper:

    """Map one key to multiple keys."""

    def __init__(self, settings) -> None:
        """Argument `settings` is profile JSON dictionary."""
        if not ("keyData" in settings[0]):
            settings = [{"keyData": {}}]
        self.settings = settings
        self.profileMap = mapProfiles(
            self.settings)  # Profile ID mapped to index in the list
        self.current_profile = (
            -1, 0)
        self.old_profiles = OrderedDict([self.current_profile])
        self.forget = []

    # New settings retunrs the first mod
    def set_new_settings(self, settings) -> None:
        """Argument `settings` is profile JSON dictionary."""
        if not ("keyData" in settings[0]):
            settings = [{'keyData': {}}]
        self.settings = settings
        self.profileMap = mapProfiles(
            self.settings)  # Profile ID mapped to index in the list
        first = self.profileMap.popitem(last=False)
        print("profileMap and first index(ID) from there => " +
              str(self.profileMap) + str(first))
        self.profileMap[first[0]] = first[1]
        self.current_profile = (
            -1, first[0])  # TODO send current mode for the front end.
        self.old_profiles = OrderedDict([self.current_profile])
        web_server_manager = WebServerManager()
        web_server_manager.get_profile_queue().put_nowait(self.current_profile[1])
        print("Lähetettiin seuraava profiili:")
        print(self.current_profile[1])
        self.forget = []

    def remap_key(self, key_event) -> List[List[int]]:
        """
        REMAPS one key to multiple keys.

        also specialized in handling the profile changes.

        Key id values are evdev id numbers.

        Returns a Tuple(List[List[int]], Bool)
        containing the output evdevID inside a list structure(List[List[int]]) and
        Bool wether to tell to remove all keys marked as pressed effectively rising them.
        """
        evdevId = key_event.code
        empty_nothing = []
        empty_key = []
        empty_key.append(empty_nothing)  # type: List[List[int]]

        # ----------------------------key up
        if key_event.value == 0:

            # key is lifted up so it nolonger needs to be inored
            if evdevId in self.forget:
                self.forget.remove(evdevId)
                return (empty_key, False)

            # return from swapped profiles
            if evdevId in self.old_profiles:
                print("returned from a mode")
                cutfrom(evdevId, self.old_profiles)
                self.current_profile = self.old_profiles.popitem(
                    last=True)  # TODO send current mode for the front end.
                self.old_profiles[
                    self.current_profile[0]] = self.current_profile[1]
                return (empty_key, True)

            # Do we actually have settings for this button
            if str(evdevId) in self.settings[self.current_profile[1]]["keyData"]:

                # the current "action" or "setting"
                keyMapping = self.settings[
                    self.current_profile[1]]["keyData"][str(evdevId)]

                if "mappedEvdevID" in keyMapping:
                    return (keyMapping["mappedEvdevID"], False)

            key = [evdevId]
            mapped_key = []
            mapped_key.append(key)  # type: List[List[int]]
            return (mapped_key, False)

        # -----------------------key down
        elif key_event.value == 1:

            # Ignore old down pressed profile switch buttons
            if evdevId in self.old_profiles:
                return (empty_key, False)

            # Ignore keys set to forget. Necessary in context of toggle switch
            # hotkey combinations.
            if evdevId in self.forget:
                return (empty_key, False)

            # Do we actually have settings for this button
            if str(evdevId) in self.settings[self.current_profile[1]]["keyData"]:

                # the current "action" or "setting"
                keyMapping = self.settings[
                    self.current_profile[1]]["keyData"][str(evdevId)]

                if "profiles" in keyMapping:
                    # if evdevId not in self.old_profiles:

                    # Toggle to different profile
                    if keyMapping["toggle"]:

                        for button in self.old_profiles:
                            if not button == -1:
                                self.forget.append(button)
                        self.current_profile = (
                            -1, self.profileMap[keyMapping["profiles"][0]])
                        # TODO send current mode for the front end.
                        print(self.current_profile)
                        self.old_profiles = OrderedDict([self.current_profile])
                        return (empty_key, True)

                    # Temporary switch while button pressed
                    self.current_profile = (
                        evdevId, self.profileMap[keyMapping["profiles"][0]])
                    # TODO send current mode for the front end.

                    self.old_profiles[
                        self.current_profile[0]] = self.current_profile[1]
                    print(self.old_profiles)
                    return (empty_key, True)

                if "mappedEvdevID" in keyMapping:
                    return (keyMapping["mappedEvdevID"], False)

        print(key_event.value)
        key = []
        key.append(evdevId)
        mapped_key = []
        mapped_key.append(key)  # type: List[List[int]]
        return(mapped_key, False)


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

    clean = False
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

        try:
            current_profile = web_server_manager.get_profile_queue().get(block=False)

        except Empty:
            pass

        for event in keyboard_manager.get_key_events():
            if event.value == 1:
                web_server_manager.get_heatmap_queue().put_nowait(event.code)

                # if key_remapper.change_profile(event.code):
                #    continue

            # profile handling
            tuple_data = key_remapper.remap_key(event)
            print(tuple_data)
            new_keys_list = tuple_data[0]
            clean = tuple_data[1]
            # profile handling

            if len(new_keys_list) == 1:
                key_list = new_keys_list[0]

                # key_down = 1
                if event.value == 1:
                    for k in key_list:
                        hid_report.add_key(k)
                    send_and_reset_if_client_disconnected(
                        hid_data_socket, hid_report, keyboard_manager)

                # key_up = 0
                elif event.value == 0:
                    for k in key_list:
                        hid_report.remove_key(k)
                    send_and_reset_if_client_disconnected(
                        hid_data_socket, hid_report, keyboard_manager)
            else:
                if event.value == 1:
                    # delays_list = key_remapper.remap_key_delays_list(
                    #    event.code)

                    for i in range(0, len(new_keys_list)):
                        key_list = new_keys_list[i]

                        for k in key_list:
                            hid_report.add_key(k)

                        send_and_reset_if_client_disconnected(
                            hid_data_socket, hid_report, keyboard_manager)

                        for k in key_list:
                            hid_report.remove_key(k)

                        send_and_reset_if_client_disconnected(
                            hid_data_socket, hid_report, keyboard_manager)

                        # if i < len(delays_list):
                        #    time.sleep(delays_list[i])
        if clean:
            hid_report.clear()


def send_and_reset_if_client_disconnected(hid_data_socket: HidDataSocket, hid_report: HidReport, keyboard_manager: KeyboardManager) -> None:
    if not hid_data_socket.send_hid_report_if_there_is_new_changes(hid_report):
        hid_data_socket.wait_connection()
        keyboard_manager.request_clear_key_events()
        hid_report.clear()


if __name__ == "__main__":
    main()
    print("main thread exitted")
