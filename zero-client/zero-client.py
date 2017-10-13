#!/bin/python3

import os

# http://www.usb.org/developers/hidpage/Hut1_12v2.pdf
# See chapter 10 for keycodes.

# The following HID Report structure is for example keyboard from Linux kernel documentation
# https://www.kernel.org/doc/Documentation/usb/gadget_hid.txt

# byte 1: modifier key bit flags from LeftContror to Right GUI (0xE0 to 0xE7)

# byte 2: some byte, not used (exists because of BIOS keyboard support?)

# byte 3-8: keycode values from 0-101


# TODO: create TCP socket

# key 'a'
HID_REPORT = [0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00]
HID_REPORT_BYTES = bytes(HID_REPORT)

EMPTY_HID_REPORT = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
EMPTY_HID_REPORT_BYTES = bytes(EMPTY_HID_REPORT)

FILE_NAME = "/dev/hidg0"

if not os.path.exists(FILE_NAME):
    print(FILE_NAME + " does not exist")
    exit(-1)

with open(FILE_NAME, "ab") as file:
    file.write(HID_REPORT_BYTES)
    file.write(EMPTY_HID_REPORT_BYTES)


print("appending to " + FILE_NAME + " ok")
