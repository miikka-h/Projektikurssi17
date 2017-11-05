#!/bin/python3

import evdev
import pyudev
from threading import Event
from queue import Queue

# keyboard detection
context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)

devinput = "/dev/input/"
event_location = ""

device_list = []

monitor.filter_by('input')

print("kissa")


def log_event(action, device):
    if 'ID_INPUT_KEYBOARD' in device:
        try:
            event_location = device.device_node
            print('{0} - {1}'.format(action, event_location))
            if event_location[0:(len(devinput))] == devinput:
                print('{0} : {1}'.format(event_location[0:(len(devinput))], devinput))
                if action == "add":
                    device_list.append(event_location)
                else:
                    try:
                        device_list.remove(event_location)
                    except ValueError:
                        pass
                print(device_list)
        except TypeError:
            pass

observer = pyudev.MonitorObserver(monitor, log_event)
observer.start()
# keyboard detection


while True:
    pass


def returnKeyboards():
    return [evdev.InputDevice(fn) for fn in evdev.list_devices()]


class FindDevices():

    def __init__(self, device_queue: Queue, exit_event: Event):
        device_queue.put_nowait(returnKeyboards)


        # if len(sys.argv) < 2:
        #    print("give evdev device file path as argument")
        #    exit(-1)

                #
        #Initialize input event reading.
        #input_device = evdev.InputDevice(sys.argv[1])
        #print(input_device)
        #
        #
