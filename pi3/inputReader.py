import evdev


class HasKeyboard:

    def __init__(self):
        print("")

    def evaluator():
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        for device in devices:
            #capabilityMap = device.capabilities(True, False)
            print(device.name + " " + device.fn)


HasKeyboard.evaluator()

class Reader:

    def __init__(self, device):
        self.device = device

    #device = evdev.InputDevice('/dev/input/event3')
    #print(device)

    def reader(self):
        for event in self.device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                print(evdev.categorize(event))
                
