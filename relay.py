import gpiozero
import time

class Relay:
    def __init__(self):
        self.RELAY_PIN = 21
        self.relay = gpiozero.OutputDevice(self.RELAY_PIN, active_high=True, initial_value=False)

    def onOff(self):
        self.on()
        time.sleep(0.5)
        self.off()
        print(f"Relay value: {self.value()}")

    def off(self):
        self.relay.off()

    def on(self):
        self.relay.on()

    def value(self):
        return self.relay.value

    


