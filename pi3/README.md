
# Keyboard server for Raspberry Pi 3

TCP server socket ports:

* `25001` USB HID report data
* `8080` Web frontend for configuration

## Setup

1. Install Python 3 and some python packages.

```
sudo apt-get install python3 python3-pip

```

```
pip3 install --upgrade pip

```

```
pip3 install --user evdev pyudev

```

If your Python 3 version is 3.4 or older, also install `typing` python package.

```
pip3 install --user typing

```

2. If you don't want to run server as root, check that your Linux user account belongs to group `input`.
(Needed for `/dev/input/event`)

```
groups your_user_name
```
To add user to a group, run this.
```
sudo usermod -a -G input your_user_name
```

3. Setup WLAN access point. [https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md](https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md)

4. Run
```
python3 main.py /dev/input/event_device_you_want_to_listen
```