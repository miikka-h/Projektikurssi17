#!/bin/python3

import evdev
import hid_report

def main():
    x = hid_report.HidReport()
    x.left_control = True
    x.add_key(evdev.ecodes.KEY_A)
    x.send()


if __name__ == "__main__":
    main()