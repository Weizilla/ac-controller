from gpiozero import LED
import board
from adafruit_bme280 import basic as adafruit_bme280
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

from device import Device


class PiDevice(Device):
    lcd_columns = 16
    lcd_rows = 2
    i2c = board.I2C()

    power_replay = LED(27)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
    lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)

    def on(self):
        self.power_replay.on()

    def off(self):
        self.power_replay.off()

    def value(self) -> int:
        return self.power_replay.value

    def temperature(self) -> int:
        temp = (self.bme280.temperature * 1.8) + 32
        if temp < 60 or temp > 100:
            raise ValueError("Temperature out of range")
        return int(temp)

    def set_lcd_message(self, line_one: str, line_two: str = ""):
        self.lcd.message = line_one + "\n" + line_two

    def set_lcd_color(self, color):
        self.lcd.color = color

