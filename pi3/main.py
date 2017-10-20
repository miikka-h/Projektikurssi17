#!/bin/python3

from queue import Queue
from threading import Thread, Event

from web_server import WebServer
import evdev
import hid_report

def main():
    x = hid_report.HidReport()
    x.left_control = True
    x.add_key(evdev.ecodes.KEY_A)
    x.send()

    exit_event = Event()

    web_server_settings = ("", 8080)
    settings_queue = Queue()

    web_server_thread = Thread(group=None, target=WebServer, args=(web_server_settings, settings_queue, exit_event))
    web_server_thread.start()

    try:
        while True:
            new_settings = settings_queue.get()
            print(str(new_settings))
    except KeyboardInterrupt:
        # handle ctrl-c
        exit_event.set()
        web_server_thread.join()

    print("main thread exitted")




if __name__ == "__main__":
    main()