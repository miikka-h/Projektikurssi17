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
    evdev.ecodes.KEY_1: 0x1E,
    evdev.ecodes.KEY_2: 0x1F,
    evdev.ecodes.KEY_3: 0x20,
    evdev.ecodes.KEY_4: 0x21,
    evdev.ecodes.KEY_5: 0x22,
    evdev.ecodes.KEY_6: 0x23,
    evdev.ecodes.KEY_7: 0x24,
    evdev.ecodes.KEY_8: 0x25,
    evdev.ecodes.KEY_9: 0x26,
    evdev.ecodes.KEY_0: 0x27,
    evdev.ecodes.KEY_ENTER: 0x28,
    evdev.ecodes.KEY_ESC: 0x29,
    evdev.ecodes.KEY_BACKSPACE: 0x2A,
    evdev.ecodes.KEY_TAB: 0x2B,
    evdev.ecodes.KEY_SPACE: 0x2C,
    evdev.ecodes.KEY_MINUS: 0x2D,
    evdev.ecodes.KEY_F1: 0x3A,
    evdev.ecodes.KEY_F2: 0x3B,
    evdev.ecodes.KEY_F3: 0x3C,
    evdev.ecodes.KEY_F4: 0x3D,
    evdev.ecodes.KEY_F5: 0x3E,
    evdev.ecodes.KEY_F6: 0x3F,
    evdev.ecodes.KEY_F7: 0x40,
    evdev.ecodes.KEY_F8: 0x41,
    evdev.ecodes.KEY_F9: 0x42,
    evdev.ecodes.KEY_F10: 0x43,
    evdev.ecodes.KEY_F11: 0x44,
    evdev.ecodes.KEY_F12: 0x45,
    evdev.ecodes.KEY_PRINT: 0x46,
    evdev.ecodes.KEY_SCROLLLOCK: 0x47,
    evdev.ecodes.KEY_PAUSE: 0x48,
    evdev.ecodes.KEY_INSERT: 0x49,
    evdev.ecodes.KEY_HOME: 0x4A,
    evdev.ecodes.KEY_PAGEUP: 0x4B,
    evdev.ecodes.KEY_DELETE: 0x4C,
    evdev.ecodes.KEY_END: 0x4D,
    evdev.ecodes.KEY_PAGEDOWN: 0x4E,
    evdev.ecodes.KEY_RIGHT: 0x4F,
    evdev.ecodes.KEY_LEFT: 0x50,
    evdev.ecodes.KEY_DOWN: 0x51,
    evdev.ecodes.KEY_UP: 0x52,
    evdev.ecodes.KEY_NUMLOCK: 0x53,
    evdev.ecodes.KEY_KPSLASH: 0x54,
    evdev.ecodes.KEY_KPASTERISK: 0x55,
    evdev.ecodes.KEY_KPMINUS: 0x56,
    evdev.ecodes.KEY_KPPLUS: 0x57,
    evdev.ecodes.KEY_KPENTER: 0x58,
    evdev.ecodes.KEY_KP1: 0x59,
    evdev.ecodes.KEY_KP2: 0x5A,
    evdev.ecodes.KEY_KP3: 0x5B,
    evdev.ecodes.KEY_KP4: 0x5C,
    evdev.ecodes.KEY_KP5: 0x5D,
    evdev.ecodes.KEY_KP6: 0x5E,
    evdev.ecodes.KEY_KP7: 0x5F,
    evdev.ecodes.KEY_KP8: 0x60,
    evdev.ecodes.KEY_KP9: 0x61,
    evdev.ecodes.KEY_KP0: 0x62,
    evdev.ecodes.KEY_APOSTROPHE: 0x63,
	#TODO find out how to refer to the rest of the keys	

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
