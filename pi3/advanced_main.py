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
        self.server_socket = None # type: socket.SocketType
        self.connection_socket = None # type: socket.SocketType
        self.address = None


    def create_socket(self) -> bool:
        """Returns False if there is socket creation error."""
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

    def set_new_settings(self, settings) -> None:
        """Argument `settings` is profile JSON dictionary."""
        self.settings = settings

    def remap_key(self, evdev_id: int) -> List[List[int]]:
        """
        Remaps one key to multiple keys.

        Key id values are evdev id numbers.

        Returns list containing lists of keys. List of keys
        represents keys that are included in one USB hid report.
        """
        list_of_hid_reports = [] # type: List[List[int]]

        single_hid = [] # type: List[int]

        # TODO: Remove for loop. That requires changes in JSON structure.

        try:
            key = self.settings[0]["keyData"][str(evdev_id)]  # TODO no parsing here. ["mappedEvdevID"]
            if isinstance(key["mappedEvdevID"], str):
                if key["mappedEvdevID"].find("|") != -1:
                        key_reports_strings = key["mappedEvdevID"].split("|")
                        for i in key_reports_strings:
                            single_hid = [int(x) for x in i.split(":")]    
                            list_of_hid_reports.append(single_hid)
                            print(list_of_hid_reports)
                else:
                        single_hid = [int(x) for x in key["mappedEvdevID"].split(":")]
                        list_of_hid_reports.append(single_hid)
                        print("list_of_hid_reports" +" kissa 1")
            else:
                single_hid.append(key["mappedEvdevID"])
                list_of_hid_reports.append(single_hid)
                print("list_of_hid_reports" + "kissa 2")
        except KeyError as error:
            single_hid.append(evdev_id)
            list_of_hid_reports.append(single_hid)
            print("list_of_hid_reports" + "kissa 3")

        return list_of_hid_reports


class KeyboardManager:
    """Read input from all availlable keyboards.

    Starts a new thread to monitor device events from Linux udev system.
    This allows adding and removing keyboards at runtime without constantly
    polling udev for new device events.

    Call `close()` to close device monitoring thread.
    """
    def __init__(self) -> None:
        self.context = pyudev.Context()
        self.device_list = [] # type: List[evdev.InputDevice]

        for keyboard in self.context.list_devices(subsystem="input", ID_INPUT_KEYBOARD=1):
            if keyboard.device_node != None:
                keyboard = evdev.InputDevice(keyboard.device_node)
                print("Keyboard '" + keyboard.name + "' added")
                self.device_list.append(keyboard)

        monitor = pyudev.Monitor.from_netlink(self.context)
        monitor.filter_by("input")

        self.exit_event = Event()
        self.event_queue = Queue() # type: Queue
        self.device_monitor_thread = Thread(group=None, target=monitor_device_events, args=(self.exit_event, self.event_queue, monitor))
        self.device_monitor_thread.start()

        self.key_event_buffer = [] # type: List[evdev.InputEvent]
        self.clear_keys = False

    def close(self) -> None:
        """Send exit event to device monitoring thread. Waits until thread is closed."""
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
    
    keypresses = ""
    keyspressed = 0
    print("waiting for settings from web server thread")
    key_remapper = KeyRemapper(web_server_manager.get_settings_queue().get())
    print("received settings from web server thread")

    keyboard_manager.request_clear_key_events()

    while True:
        time.sleep(0.001)

        keyboard_manager.check_device_events()

        try:
            new_settings = web_server_manager.get_settings_queue().get(block=False)
            key_remapper.set_new_settings(new_settings)
        except Empty:
            pass

        for event in keyboard_manager.get_key_events():
            heatmap_key = str(event)[str(event).find("code")+ 5 :str(event).find("code") + 7]
            print(event)            
            new_keys_list = key_remapper.remap_key(event.code)
            
            if len(new_keys_list) == 1:
                key_list = new_keys_list[0]
                
                # key_down = 1
                if event.value == 1:
                    for k in key_list:
                        hid_report.add_key(k)
                        keypresses += heatmap_key+"|"
                        print(keypresses)
                        keyspressed += 1
                        if keyspressed == 10:
                            f = open('heatmap_data.txt','w')
                            f.write(keypresses)
                            f.close()
                            heatmap()
                            keyspressed = 0
                # key_up = 0
                elif event.value == 0:
                    for k in key_list:
                        hid_report.remove_key(k)
            else:
                if event.value == 1:
                    for report in new_keys_list:
                        key_list = report
                        print(key_list)
                        for k in key_list:
                            hid_report.add_key(k)
                            keypresses += heatmap_key+"|"
                            keyspressed += 1
                            if keyspressed == 10:
                                f = open('heatmap_data.txt','w')
                                f.write(keypresses)
                                f.close()
                                heatmap()
                                keyspressed = 0
                        send_and_reset_if_client_disconnected(hid_data_socket, hid_report, keyboard_manager)
                        for k in key_list:
                            hid_report.remove_key(k)
                        send_and_reset_if_client_disconnected(hid_data_socket, hid_report, keyboard_manager)    
                            #break    

                  

                #pass
                # TODO: Handle more complicated key remaps.
        send_and_reset_if_client_disconnected(hid_data_socket, hid_report, keyboard_manager)
        #break
    f.close()
    
    
  
def send_and_reset_if_client_disconnected(hid_data_socket: HidDataSocket, hid_report: HidReport, keyboard_manager: KeyboardManager) -> None:           
    if not hid_data_socket.send_hid_report_if_there_is_new_changes(hid_report):
        hid_data_socket.wait_connection()
        keyboard_manager.request_clear_key_events()
        hid_report.clear()
        

def heatmap() -> None:
    
    heatmap_stats = {} 
    

    with open("heatmap_stats.txt", 'r') as statfile:
        help_dict = statfile.read().strip('{').strip('}').split(',')
        for entry in help_dict:
            (key, val) = entry.rstrip("\n").split(':')
            heatmap_stats[int(key)] = int(val)
    statfile.close()        

    print(heatmap_stats)
    
    hmdata = open("heatmap_data.txt", 'r')
    statfile = open("heatmap_stats.txt", 'w')
    key_presses = hmdata.read().split('|')
    hmdata.close()
    print(key_presses)

    for kpress in key_presses:
        if kpress is not "":
            heatmap_stats[int(kpress)] = heatmap_stats[int((kpress).rstrip())]
            heatmap_stats[int(kpress)] += 1
            print(heatmap_stats[int(kpress)])
        
    print(heatmap_stats)
    
    if heatmap_stats is not "":
        statfile.write(str(heatmap_stats))
    statfile.close()


if __name__ == "__main__":
    main()
    print("main thread exitted")
