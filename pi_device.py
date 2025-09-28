from gpiozero import LED

from device import Device


class PiDevice(Device):
    led = LED(27)

    def on(self):
        self.led.on()

    def off(self):
        self.led.off()

    def value(self) -> int:
        return self.led.value

    def temperature(self) -> int:
        return 77

