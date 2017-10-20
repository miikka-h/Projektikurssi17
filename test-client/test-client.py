#!/bin/python3

import sys
import socket

HID_REPORT_SIZE_BYTES = 8

if len(sys.argv) < 2:
    print("give server address and server port number as arguments")
    exit(-1)


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
            exit(-1)

        print("data: {0:#b} ".format(data[0]), end='')
        for i in range(1,8):
            print("{0:#x} ".format(data[i]), end='')

        print()
except OSError as error:
    print("error: " + error.strerror)
    s.close()
except KeyboardInterrupt:
    s.close()

