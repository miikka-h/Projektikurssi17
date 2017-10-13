# Zero-client

This directory contains

* Bash-shell script that starts Raspberry Pi Zero USB keyboard and ethernet network gadget and zero-client.py
* Zero-client Python 3 application that writes data from TCP socket to a file.

Currently zero-client.py only writes HID report for key `a` to file `/dev/hidg0`.

# Running

Note that this only works on Raspberry Pi Zero or Zero W.

1. Copy `zero-client.py`, `copy-usb-hid-description.py`, `start.sh` to the root of the filesystem `/`.

2. Create directory `/configfs_dir`.

3. Run `start.sh` as root.