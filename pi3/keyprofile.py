import evdev

settings = {
    "profileName": "Profile-0",
    "profileID": 0,
    "keyData": [
        {
            "displayName": "Esc",
            "evdevName": "KEY_ESC",
            "EvdevID": 1,
            "mappedEvdevName": "KEY_ESC",
            "mappedEvdevID": 1
        },
        {
            "displayName": "F1",
            "evdevName": "KEY_F1",
            "EvdevID": 59,
            "mappedEvdevName": "KEY_F1",
            "mappedEvdevID": 59
        },
        {
            "displayName": "F2",
            "evdevName": "KEY_F2",
            "EvdevID": 60,
            "mappedEvdevName": "KEY_F2",
            "mappedEvdevID": 60
        },
        {
            "displayName": "F3",
            "evdevName": "KEY_F3",
            "EvdevID": 61,
            "mappedEvdevName": "KEY_F3",
            "mappedEvdevID": 61
        },
        {
            "displayName": "F4",
            "evdevName": "KEY_F4",
            "EvdevID": 62,
            "mappedEvdevName": "KEY_F4",
            "mappedEvdevID": 62
        },
        {
            "displayName": "F5",
            "evdevName": "KEY_F5",
            "EvdevID": 63,
            "mappedEvdevName": "KEY_F5",
            "mappedEvdevID": 63
        },
        {
            "displayName": "F6",
            "evdevName": "KEY_F6",
            "EvdevID": 64,
            "mappedEvdevName": "KEY_F6",
            "mappedEvdevID": 64
        },
        {
            "displayName": "F7",
            "evdevName": "KEY_F7",
            "EvdevID": 65,
            "mappedEvdevName": "KEY_F7",
            "mappedEvdevID": 65
        },
        {
            "displayName": "F8",
            "evdevName": "KEY_F8",
            "EvdevID": 66,
            "mappedEvdevName": "KEY_F8",
            "mappedEvdevID": 66
        },
        {
            "displayName": "F9",
            "evdevName": "KEY_F9",
            "EvdevID": 67,
            "mappedEvdevName": "KEY_F9",
            "mappedEvdevID": 67
        },
        {
            "displayName": "F10",
            "evdevName": "KEY_F10",
            "EvdevID": 68,
            "mappedEvdevName": "KEY_F10",
            "mappedEvdevID": 68
        },
        {
            "displayName": "F11",
            "evdevName": "KEY_F11",
            "EvdevID": 87,
            "mappedEvdevName": "KEY_F11",
            "mappedEvdevID": 87
        },
        {
            "displayName": "F12",
            "evdevName": "KEY_F12",
            "EvdevID": 88,
            "mappedEvdevName": "KEY_F12",
            "mappedEvdevID": 88
        },
        {
            "displayName": "Print",
            "evdevName": "KEY_PRINT",
            "EvdevID": 210,
            "mappedEvdevName": "KEY_PRINT",
            "mappedEvdevID": 210
        },
        {
            "displayName": "ScrollLock",
            "evdevName": "KEY_SCROLLLOCK",
            "EvdevID": 70,
            "mappedEvdevName": "KEY_SCROLLLOCK",
            "mappedEvdevID": 70
        },
        {
            "displayName": "Pause",
            "evdevName": "KEY_PAUSE",
            "EvdevID": 119,
            "mappedEvdevName": "KEY_PAUSE",
            "mappedEvdevID": 119
        },
        {
            "displayName": "§",
            "evdevName": "KEY_GRAVE",
            "EvdevID": 41,
            "mappedEvdevName": "KEY_GRAVE",
            "mappedEvdevID": 41
        },
        {
            "displayName": "1",
            "evdevName": "KEY_1",
            "EvdevID": 2,
            "mappedEvdevName": "KEY_1",
            "mappedEvdevID": 2
        },
        {
            "displayName": "2",
            "evdevName": "KEY_2",
            "EvdevID": 3,
            "mappedEvdevName": "KEY_2",
            "mappedEvdevID": 3
        },
        {
            "displayName": "3",
            "evdevName": "KEY_3",
            "EvdevID": 4,
            "mappedEvdevName": "KEY_3",
            "mappedEvdevID": 4
        },
        {
            "displayName": "4",
            "evdevName": "KEY_4",
            "EvdevID": 5,
            "mappedEvdevName": "KEY_4",
            "mappedEvdevID": 5
        },
        {
            "displayName": "5",
            "evdevName": "KEY_5",
            "EvdevID": 6,
            "mappedEvdevName": "KEY_5",
            "mappedEvdevID": 6
        },
        {
            "displayName": "6",
            "evdevName": "KEY_6",
            "EvdevID": 7,
            "mappedEvdevName": "KEY_6",
            "mappedEvdevID": 7
        },
        {
            "displayName": "7",
            "evdevName": "KEY_7",
            "EvdevID": 8,
            "mappedEvdevName": "KEY_7",
            "mappedEvdevID": 8
        },
        {
            "displayName": "8",
            "evdevName": "KEY_8",
            "EvdevID": 9,
            "mappedEvdevName": "KEY_8",
            "mappedEvdevID": 9
        },
        {
            "displayName": "9",
            "evdevName": "KEY_9",
            "EvdevID": 10,
            "mappedEvdevName": "KEY_9",
            "mappedEvdevID": 10
        },
        {
            "displayName": "0",
            "evdevName": "KEY_0",
            "EvdevID": 11,
            "mappedEvdevName": "KEY_0",
            "mappedEvdevID": 11
        },
        {
            "displayName": "+",
            "evdevName": "KEY_MINUS",
            "EvdevID": 12,
            "mappedEvdevName": "KEY_MINUS",
            "mappedEvdevID": 12
        },
        {
            "displayName": "´",
            "evdevName": "KEY_EQUAL",
            "EvdevID": 13,
            "mappedEvdevName": "KEY_EQUAL",
            "mappedEvdevID": 13
        },
        {
            "displayName": "<=",
            "evdevName": "KEY_BACKSPACE",
            "EvdevID": 14,
            "mappedEvdevName": "KEY_BACKSPACE",
            "mappedEvdevID": 14
        },
        {
            "displayName": "Insert",
            "evdevName": "KEY_INSERT",
            "EvdevID": 110,
            "mappedEvdevName": "KEY_INSERT",
            "mappedEvdevID": 110
        },
        {
            "displayName": "Home",
            "evdevName": "KEY_HOME",
            "EvdevID": 102,
            "mappedEvdevName": "KEY_HOME",
            "mappedEvdevID": 102
        },
        {
            "displayName": "PageUp",
            "evdevName": "KEY_PAGEUP",
            "EvdevID": 104,
            "mappedEvdevName": "KEY_PAGEUP",
            "mappedEvdevID": 104
        },
        {
            "displayName": "NumLock",
            "evdevName": "KEY_NUMLOCK",
            "EvdevID": 69,
            "mappedEvdevName": "KEY_NUMLOCK",
            "mappedEvdevID": 69
        },
        {
            "displayName": "/",
            "evdevName": "KEY_KPSLASH",
            "EvdevID": 98,
            "mappedEvdevName": "KEY_KPSLASH",
            "mappedEvdevID": 98
        },
        {
            "displayName": "*",
            "evdevName": "KEY_KPASTERISK",
            "EvdevID": 55,
            "mappedEvdevName": "KEY_KPASTERISK",
            "mappedEvdevID": 55
        },
        {
            "displayName": "kp-",
            "evdevName": "KEY_KPMINUS",
            "EvdevID": 74,
            "mappedEvdevName": "KEY_KPMINUS",
            "mappedEvdevID": 74
        },
        {
            "displayName": "Tab",
            "evdevName": "KEY_TAB",
            "EvdevID": 15,
            "mappedEvdevName": "KEY_TAB",
            "mappedEvdevID": 15
        },
        {
            "displayName": "q",
            "evdevName": "KEY_Q",
            "EvdevID": 16,
            "mappedEvdevName": "KEY_Q",
            "mappedEvdevID": 16
        },
        {
            "displayName": "w",
            "evdevName": "KEY_W",
            "EvdevID": 17,
            "mappedEvdevName": "KEY_W",
            "mappedEvdevID": 17
        },
        {
            "displayName": "e",
            "evdevName": "KEY_E",
            "EvdevID": 18,
            "mappedEvdevName": "KEY_E",
            "mappedEvdevID": 18
        },
        {
            "displayName": "r",
            "evdevName": "KEY_R",
            "EvdevID": 19,
            "mappedEvdevName": "KEY_R",
            "mappedEvdevID": 19
        },
        {
            "displayName": "t",
            "evdevName": "KEY_T",
            "EvdevID": 20,
            "mappedEvdevName": "KEY_T",
            "mappedEvdevID": 20
        },
        {
            "displayName": "y",
            "evdevName": "KEY_Y",
            "EvdevID": 21,
            "mappedEvdevName": "asffasf",
            "mappedEvdevID": 21
        },
        {
            "displayName": "u",
            "evdevName": "KEY_U",
            "EvdevID": 22,
            "mappedEvdevName": "KEY_U",
            "mappedEvdevID": 22
        },
        {
            "displayName": "i",
            "evdevName": "KEY_I",
            "EvdevID": 23,
            "mappedEvdevName": "KEY_I",
            "mappedEvdevID": 23
        },
        {
            "displayName": "o",
            "evdevName": "KEY_O",
            "EvdevID": 24,
            "mappedEvdevName": "KEY_O",
            "mappedEvdevID": 24
        },
        {
            "displayName": "p",
            "evdevName": "KEY_P",
            "EvdevID": 25,
            "mappedEvdevName": "KEY_P",
            "mappedEvdevID": 25
        },
        {
            "displayName": "å",
            "evdevName": "KEY_LEFTBRACE",
            "EvdevID": 26,
            "mappedEvdevName": "KEY_LEFTBRACE",
            "mappedEvdevID": 26
        },
        {
            "displayName": "^",
            "evdevName": "KEY_RIGHTBRACE",
            "EvdevID": 27,
            "mappedEvdevName": "KEY_RIGHTBRACE",
            "mappedEvdevID": 27
        },
        {
            "displayName": "Enter",
            "evdevName": "KEY_ENTER",
            "EvdevID": 28,
            "mappedEvdevName": "KEY_ENTER",
            "mappedEvdevID": 28
        },
        {
            "displayName": "Del",
            "evdevName": "KEY_DELETE",
            "EvdevID": 111,
            "mappedEvdevName": "KEY_DELETE",
            "mappedEvdevID": 111
        },
        {
            "displayName": "End",
            "evdevName": "KEY_END",
            "EvdevID": 107,
            "mappedEvdevName": "KEY_END",
            "mappedEvdevID": 107
        },
        {
            "displayName": "PageDown",
            "evdevName": "KEY_PAGEDOWN",
            "EvdevID": 109,
            "mappedEvdevName": "KEY_PAGEDOWN",
            "mappedEvdevID": 109
        },
        {
            "displayName": "kp7",
            "evdevName": "KEY_KP7",
            "EvdevID": 71,
            "mappedEvdevName": "KEY_KP7",
            "mappedEvdevID": 71
        },
        {
            "displayName": "kp8",
            "evdevName": "KEY_KP8",
            "EvdevID": 72,
            "mappedEvdevName": "KEY_KP8",
            "mappedEvdevID": 72
        },
        {
            "displayName": "kp9",
            "evdevName": "KEY_KP9",
            "EvdevID": 73,
            "mappedEvdevName": "KEY_KP9",
            "mappedEvdevID": 73
        },
        {
            "displayName": "kp+",
            "evdevName": "KEY_KPPLUS",
            "EvdevID": 78,
            "mappedEvdevName": "KEY_KPPLUS",
            "mappedEvdevID": 78
        },
        {
            "displayName": "CapsLock",
            "evdevName": "KEY_CAPSLOCK",
            "EvdevID": 58,
            "mappedEvdevName": "KEY_CAPSLOCK",
            "mappedEvdevID": 58
        },
        {
            "displayName": "a",
            "evdevName": "KEY_A",
            "EvdevID": 30,
            "mappedEvdevName": "KEY_A",
            "mappedEvdevID": 30
        },
        {
            "displayName": "s",
            "evdevName": "KEY_S",
            "EvdevID": 31,
            "mappedEvdevName": "KEY_S",
            "mappedEvdevID": 31
        },
        {
            "displayName": "d",
            "evdevName": "KEY_D",
            "EvdevID": 32,
            "mappedEvdevName": "KEY_D",
            "mappedEvdevID": 32
        },
        {
            "displayName": "f",
            "evdevName": "KEY_F",
            "EvdevID": 33,
            "mappedEvdevName": "KEY_F",
            "mappedEvdevID": 33
        },
        {
            "displayName": "g",
            "evdevName": "KEY_G",
            "EvdevID": 34,
            "mappedEvdevName": "KEY_G",
            "mappedEvdevID": 34
        },
        {
            "displayName": "h",
            "evdevName": "KEY_H",
            "EvdevID": 35,
            "mappedEvdevName": "KEY_H",
            "mappedEvdevID": 35
        },
        {
            "displayName": "j",
            "evdevName": "KEY_J",
            "EvdevID": 36,
            "mappedEvdevName": "KEY_J",
            "mappedEvdevID": 36
        },
        {
            "displayName": "k",
            "evdevName": "KEY_K",
            "EvdevID": 37,
            "mappedEvdevName": "KEY_K",
            "mappedEvdevID": 37
        },
        {
            "displayName": "l",
            "evdevName": "KEY_L",
            "EvdevID": 38,
            "mappedEvdevName": "KEY_L",
            "mappedEvdevID": 38
        },
        {
            "displayName": "ö",
            "evdevName": "KEY_SEMICOLON",
            "EvdevID": 39,
            "mappedEvdevName": "KEY_SEMICOLON",
            "mappedEvdevID": 39
        },
        {
            "displayName": "ä",
            "evdevName": "KEY_APOSTROPHE",
            "EvdevID": 40,
            "mappedEvdevName": "KEY_APOSTROPHE",
            "mappedEvdevID": 40
        },
        {
            "displayName": "'",
            "evdevName": "KEY_BACKSLASH",
            "EvdevID": 43,
            "mappedEvdevName": "KEY_BACKSLASH",
            "mappedEvdevID": 43
        },
        {
            "displayName": "kp4",
            "evdevName": "KEY_KP4",
            "EvdevID": 75,
            "mappedEvdevName": "KEY_KP4",
            "mappedEvdevID": 75
        },
        {
            "displayName": "kp5",
            "evdevName": "KEY_KP5",
            "EvdevID": 76,
            "mappedEvdevName": "KEY_KP5",
            "mappedEvdevID": 76
        },
        {
            "displayName": "kp6",
            "evdevName": "KEY_KP6",
            "EvdevID": 77,
            "mappedEvdevName": "KEY_KP6",
            "mappedEvdevID": 77
        },
        {
            "displayName": "LeftShift",
            "evdevName": "KEY_LEFTSHIFT",
            "EvdevID": 42,
            "mappedEvdevName": "KEY_LEFTSHIFT",
            "mappedEvdevID": 42
        },
        {
            "displayName": "<",
            "evdevName": "KEY_102ND",
            "EvdevID": 86,
            "mappedEvdevName": "KEY_102ND",
            "mappedEvdevID": 86
        },
        {
            "displayName": "z",
            "evdevName": "KEY_Z",
            "EvdevID": 44,
            "mappedEvdevName": "KEY_Z",
            "mappedEvdevID": 44
        },
        {
            "displayName": "x",
            "evdevName": "KEY_X",
            "EvdevID": 45,
            "mappedEvdevName": "KEY_X",
            "mappedEvdevID": 45
        },
        {
            "displayName": "c",
            "evdevName": "KEY_C",
            "EvdevID": 46,
            "mappedEvdevName": "KEY_C",
            "mappedEvdevID": 46
        },
        {
            "displayName": "v",
            "evdevName": "KEY_V",
            "EvdevID": 47,
            "mappedEvdevName": "KEY_V",
            "mappedEvdevID": 47
        },
        {
            "displayName": "b",
            "evdevName": "KEY_B",
            "EvdevID": 48,
            "mappedEvdevName": "KEY_B",
            "mappedEvdevID": 48
        },
        {
            "displayName": "n",
            "evdevName": "KEY_N",
            "EvdevID": 49,
            "mappedEvdevName": "KEY_N",
            "mappedEvdevID": 49
        },
        {
            "displayName": "m",
            "evdevName": "KEY_M",
            "EvdevID": 50,
            "mappedEvdevName": "KEY_M",
            "mappedEvdevID": 50
        },
        {
            "displayName": ",",
            "evdevName": "KEY_COMMA",
            "EvdevID": 51,
            "mappedEvdevName": "KEY_COMMA",
            "mappedEvdevID": 51
        },
        {
            "displayName": ".",
            "evdevName": "KEY_DOT",
            "EvdevID": 52,
            "mappedEvdevName": "KEY_DOT",
            "mappedEvdevID": 52
        },
        {
            "displayName": "-",
            "evdevName": "KEY_SLASH",
            "EvdevID": 53,
            "mappedEvdevName": "KEY_SLASH",
            "mappedEvdevID": 53
        },
        {
            "displayName": "Shift",
            "evdevName": "KEY_RIGHTSHIFT",
            "EvdevID": 54,
            "mappedEvdevName": "KEY_RIGHTSHIFT",
            "mappedEvdevID": 54
        },
        {
            "displayName": "Up",
            "evdevName": "KEY_UP",
            "EvdevID": 103,
            "mappedEvdevName": "KEY_UP",
            "mappedEvdevID": 103
        },
        {
            "displayName": "kp1",
            "evdevName": "KEY_KP1",
            "EvdevID": 79,
            "mappedEvdevName": "KEY_KP1",
            "mappedEvdevID": 79
        },
        {
            "displayName": "kp2",
            "evdevName": "KEY_KP2",
            "EvdevID": 80,
            "mappedEvdevName": "KEY_KP2",
            "mappedEvdevID": 80
        },
        {
            "displayName": "kp3",
            "evdevName": "KEY_KP3",
            "EvdevID": 81,
            "mappedEvdevName": "KEY_KP3",
            "mappedEvdevID": 81
        },
        {
            "displayName": "kpEnter",
            "evdevName": "KEY_KPENTER",
            "EvdevID": 96,
            "mappedEvdevName": "KEY_KPENTER",
            "mappedEvdevID": 96
        },
        {
            "displayName": "LeftCtrl",
            "evdevName": "KEY_LEFTCTRL",
            "EvdevID": 29,
            "mappedEvdevName": "KEY_LEFTCTRL",
            "mappedEvdevID": 29
        },
        {
            "displayName": "Win",
            "evdevName": "KEY_LEFTMETA",
            "EvdevID": 125,
            "mappedEvdevName": "KEY_LEFTMETA",
            "mappedEvdevID": 125
        },
        {
            "displayName": "Alt",
            "evdevName": "KEY_LEFTALT",
            "EvdevID": 56,
            "mappedEvdevName": "KEY_LEFTALT",
            "mappedEvdevID": 56
        },
        {
            "displayName": "Space",
            "evdevName": "KEY_SPACE",
            "EvdevID": 57,
            "mappedEvdevName": "KEY_SPACE",
            "mappedEvdevID": 57
        },
        {
            "displayName": "Alt",
            "evdevName": "KEY_RIGHTALT",
            "EvdevID": 100,
            "mappedEvdevName": "KEY_RIGHTALT",
            "mappedEvdevID": 100
        },
        {
            "displayName": "Win",
            "evdevName": "KEY_RIGHTMETA",
            "EvdevID": 126,
            "mappedEvdevName": "KEY_RIGHTMETA",
            "mappedEvdevID": 126
        },
        {
            "displayName": "Menu",
            "evdevName": "KEY_MENU",
            "EvdevID": 139,
            "mappedEvdevName": "KEY_MENU",
            "mappedEvdevID": 139
        },
        {
            "displayName": "Ctrl",
            "evdevName": "KEY_RIGHTCTRL",
            "EvdevID": 97,
            "mappedEvdevName": "KEY_RIGHTCTRL",
            "mappedEvdevID": 97
        },
        {
            "displayName": "Left",
            "evdevName": "KEY_LEFT",
            "EvdevID": 105,
            "mappedEvdevName": "KEY_LEFT",
            "mappedEvdevID": 105
        },
        {
            "displayName": "Down",
            "evdevName": "KEY_DOWN",
            "EvdevID": 108,
            "mappedEvdevName": "KEY_DOWN",
            "mappedEvdevID": 108
        },
        {
            "displayName": "Right",
            "evdevName": "KEY_RIGHT",
            "EvdevID": 106,
            "mappedEvdevName": "KEY_RIGHT",
            "mappedEvdevID": 106
        },
        {
            "displayName": "kp0",
            "evdevName": "KEY_KP0",
            "EvdevID": 82,
            "mappedEvdevName": "KEY_KP0",
            "mappedEvdevID": 82
        },
        {
            "displayName": "kp,",
            "evdevName": "KEY_KPDOT",
            "EvdevID": 83,
            "mappedEvdevName": "KEY_KPDOT",
            "mappedEvdevID": 83
        }
    ]
}