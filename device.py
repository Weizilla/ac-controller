from abc import ABC, abstractmethod

class Device(ABC):
    @abstractmethod
    def on(self):
        pass

    @abstractmethod
    def off(self):
        pass

    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def temperature(self):
        pass

    @abstractmethod
    def set_lcd_message(self, line_one: str, line_two: str = ""):
        pass

    @abstractmethod
    def set_lcd_color(self, color):
        pass
