

import evdev


class HidReport:

    def __init__(self):
        self.clear()

    def clear(self):
        self.left_control = False
        self.left_shift = False
        self.left_alt = False
        self.left_gui = False
        self.right_control = False
        self.right_shift = False
        self.right_alt = False
        self.right_gui = False

        self.keycodes = bytearray(6)





