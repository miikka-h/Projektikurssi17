# Zero-client

This directory contains

* Bash-shell script that starts Raspberry Pi Zero USB keyboard gadget and zero-client.py
    * Script options: `--enable-usb-ethernet-gadget`
    * Default server address and port for zero-client.py are `192.168.0.1` and `25001`
* Zero-client Python 3 application that writes USB HID report data from TCP socket to a file at `/dev/hidg0`.
    * Server address and port are required arguments.
    * If connection to server is lost, Zero-client will try to reconnect at every 5 seconds.

Note that Zero-client is designed to only work on Raspberry Pi Zero or Zero W.

# Setup

1. Configure WLAN, [https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md), If you run Zero-client on Raspberry Pi Zero there
is no WLAN chip included on the board, so you probably have use Raspberry Pi Zero as USB ethernet gadget to get connection to the server.

2. Copy `zero-client.py`, `copy-usb-hid-description.py`, `start.sh` to the root of the filesystem `/`.

3. Add line `bash -eu /start.sh &` to `rc.local` before `exit` command. This will make
Zero-client to automatically start at boot. See also: [https://www.raspberrypi.org/documentation/linux/usage/rc-local.md](https://www.raspberrypi.org/documentation/linux/usage/rc-local.md)

4. Reboot Raspberry Pi.

5. Connect Raspberry Pi to some computer with USB cable.
