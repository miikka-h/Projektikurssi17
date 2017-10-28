#!/bin/python3

import evdev
import pyudev
from threading import Event
from queue import Queue

# täällä tapahtuu jotakin VVVVVV
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)

monitor.filter_by('input')

print("kissa")


def log_event(action, device):
    if 'ID_INPUT_KEYBOARD' in device:
        print('{0} - {1}'.format(action, device.get('ID_INPUT_KEYBOARD')))


observer = pyudev.MonitorObserver(monitor, log_event)
observer.start()
# täällä tapahtuu jotakin ^^^^^^^


while True:
    pass


def returnKeyboards():
    return [evdev.InputDevice(fn) for fn in evdev.list_devices()]


class FindDevices():

    def __init__(self, device_queue: Queue, exit_event: Event):
        device_queue.put_nowait(returnKeyboards)
