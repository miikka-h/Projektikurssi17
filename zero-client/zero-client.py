#!/bin/python3

import os
import sys
import socket
import time

# http://www.usb.org/developers/hidpage/Hut1_12v2.pdf
# See chapter 10 for keycodes.

# The following HID Report structure is for example keyboard from Linux kernel documentation
# https://www.kernel.org/doc/Documentation/usb/gadget_hid.txt

# byte 1: modifier key bit flags from LeftContror to Right GUI (0xE0 to 0xE7)

# byte 2: some byte, not used (exists because of BIOS keyboard support?)

# byte 3-8: keycode values from 0-101

FILE_NAME = "/dev/hidg0"
HID_REPORT_SIZE_BYTES = 8

# Functions
def try_to_connect(socket_object: socket.SocketType, server_address: str, port_number: int) -> bool:
    try:
        socket_object.connect((server_address, port_number))
    except OSError as error:
        print("error: " + error.strerror)
        return False
    return True

def connection_retry_loop(socket_object: socket.SocketType, server_address: str, port_number: int) -> None:
    while True:
        if try_to_connect(socket_object, server_address, port_number):
            print("connected to the server")
            break
        else:
            print("trying to reconnect to the server in 5 seconds")
            time.sleep(5.0)

def main() -> None:
    # Check arguments

    if len(sys.argv) <= 2:
        print("give server address and server port number as arguments")
        exit(-1)

    # Open file.

    if not os.path.exists(FILE_NAME):
        print(FILE_NAME + " does not exist")
        exit(-1)

    file = open(FILE_NAME, "ab")

    # Create socket.

    socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = sys.argv[1]
    port_number = int(sys.argv[2])

    try:
        print("trying to connect to the server")
        connection_retry_loop(socket_object, server_address, port_number)

        while True:
            data = socket_object.recv(HID_REPORT_SIZE_BYTES)
            byte_count = len(data)

            if byte_count == 0:
                print("server disconnected")
                print("trying to reconnect")
                socket_object.close()
                socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection_retry_loop(socket_object, server_address, port_number)
            elif byte_count != HID_REPORT_SIZE_BYTES:
                print("error: USB HID report size " + str(byte_count) + " bytes is unsupported")
                socket_object.close()
                file.close()
                exit(-1)
            else:
                # No errors
                file.write(data)
                file.flush()

    except OSError as error:
        print("error: " + error.strerror)
        file.close()
        socket_object.close()
    except KeyboardInterrupt:
        file.close()
        socket_object.close()
