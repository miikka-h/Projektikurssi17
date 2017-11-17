#!/bin/python3

import sys
import socket
import time

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
    if len(sys.argv) <= 2:
        print("give server address and server port number as arguments")
        exit(-1)

    socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = sys.argv[1]
    port_number = int(sys.argv[2])

    try:
        print("trying to connect to the server")
        connection_retry_loop(socket_object, server_address, port_number)

        while True:
            data = socket_object.recv(HID_REPORT_SIZE_BYTES)
            byte_count = len(data)

            # Lets do some error handling.

            if byte_count == 0:
                print("server disconnected ")
                print("trying to reconnect")
                socket_object.close()
                socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection_retry_loop(socket_object, server_address, port_number)
            elif byte_count != HID_REPORT_SIZE_BYTES:
                print("error: USB HID report size " + str(byte_count) + " bytes is unsupported")
                socket_object.close()
                exit(-1)
            else:
                # No errors
                if data[0] == 0:
                    print("data:            ", end='')
                else:
                    print("data: {0:0=#10b} ".format(data[0]), end='')

                print("| ", end='')

                for i in range(2, 8):
                    if data[i] == 0:
                        print("     ", end='')
                    else:
                        print("{0:0=#4x} ".format(data[i]), end='')
                print("|")

    except OSError as error:
        print("error: " + error.strerror)
        socket_object.close()
    except KeyboardInterrupt:
        socket_object.close()


# Start main function

if __name__ == "__main__":
    main()