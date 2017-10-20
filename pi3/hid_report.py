

import evdev

EVDEV_TO_HID_MAP = {
    evdev.ecodes.KEY_A: 0x04,
    evdev.ecodes.KEY_B: 0x05,
    evdev.ecodes.KEY_C: 0x06,
    evdev.ecodes.KEY_D: 0x07,
    evdev.ecodes.KEY_E: 0x08,
    evdev.ecodes.KEY_F: 0x09,
    evdev.ecodes.KEY_G: 0x0A,
    evdev.ecodes.KEY_H: 0x0B,
    evdev.ecodes.KEY_I: 0x0C,
    evdev.ecodes.KEY_J: 0x0D,
    evdev.ecodes.KEY_K: 0x0E,
    evdev.ecodes.KEY_L: 0x0F,
    evdev.ecodes.KEY_M: 0x10,
    evdev.ecodes.KEY_N: 0x11,
    evdev.ecodes.KEY_O: 0x12,
    evdev.ecodes.KEY_P: 0x13,
    evdev.ecodes.KEY_Q: 0x14,
    evdev.ecodes.KEY_R: 0x15,
    evdev.ecodes.KEY_S: 0x16,
    evdev.ecodes.KEY_T: 0x17,
    evdev.ecodes.KEY_U: 0x18,
    evdev.ecodes.KEY_V: 0x19,
    evdev.ecodes.KEY_W: 0x1A,
    evdev.ecodes.KEY_X: 0x1B,
    evdev.ecodes.KEY_Y: 0x1C,
    evdev.ecodes.KEY_Z: 0x1D,
}


class HidReport:

    def __init__(self) -> None:
        self.clear()

    def clear(self) -> None:
        self.left_control = False
        self.left_shift = False
        self.left_alt = False
        self.left_gui = False
        self.right_control = False
        self.right_shift = False
        self.right_alt = False
        self.right_gui = False

        self.keycodes = {}

        self.report = bytearray(8)

    def modifier_keys(self) -> bytes:
        bit_flag = 0x00

        if self.left_control:
            bit_flag = bit_flag | 0b10000000
        if self.left_shift:
            bit_flag = bit_flag | 0b01000000
        if self.left_alt:
            bit_flag = bit_flag | 0b00100000
        if self.left_gui:
            bit_flag = bit_flag | 0b00010000
        if self.right_control:
            bit_flag = bit_flag | 0b00001000
        if self.right_shift:
            bit_flag = bit_flag | 0b00000100
        if self.right_alt:
            bit_flag = bit_flag | 0b00000010
        if self.right_gui:
            bit_flag = bit_flag | 0b00000001

        return bytes([bit_flag])

    def add_key(self, evdev_key: int) -> None:
        if len(self.keycodes) >= 6:
            return

        try:
            self.keycodes[evdev_key] = EVDEV_TO_HID_MAP[evdev_key]
        except KeyError:
            print("unknown key: " + str(evdev_key))


    def remove_key(self, evdev_key: int) -> None:
        try:
            del self.keycodes[evdev_key]
        except KeyError:
            print("unknown key: " + str(evdev_key))

    def update_report(self) -> None:
        self.report[0] = self.modifier_keys()[0]

        i = 2

        for _, item in self.keycodes.items():
            self.report[i] = item
            i += 1

        for j in range(i, 8):
            self.report[j] = 0x00




