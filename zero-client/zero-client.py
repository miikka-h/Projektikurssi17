#!/bin/python3

import os
import sys
import socket

# http://www.usb.org/developers/hidpage/Hut1_12v2.pdf
# See chapter 10 for keycodes.

# The following HID Report structure is for example keyboard from Linux kernel documentation
# https://www.kernel.org/doc/Documentation/usb/gadget_hid.txt

# byte 1: modifier key bit flags from LeftContror to Right GUI (0xE0 to 0xE7)

# byte 2: some byte, not used (exists because of BIOS keyboard support?)

# byte 3-8: keycode values from 0-101


# Check arguments

if len(sys.argv) <= 2:
    print("give server address and server port number as arguments")
    exit(-1)



# Open file.

FILE_NAME = "/dev/hidg0"

if not os.path.exists(FILE_NAME):
    print(FILE_NAME + " does not exist")
    exit(-1)

file = open(FILE_NAME, "ab")

# Connect to server

HID_REPORT_SIZE_BYTES = 8

print("trying to connect to the server")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((sys.argv[1], int(sys.argv[2])))

print("connected to to server")

try:
    while True:
        data = s.recv(HID_REPORT_SIZE_BYTES)
        byte_count = len(data)

        if byte_count < HID_REPORT_SIZE_BYTES:
            print("received " + str(byte_count) + " bytes")
            print("error: received less than " + str(HID_REPORT_SIZE_BYTES) + " bytes")
            s.close()
            file.close()
            exit(-1)

        file.write(data)
        file.flush()
except OSError as error:
    print("error: " + error.strerror)
    file.close()
    s.close()
except KeyboardInterrupt:
    file.close()
    s.close()






