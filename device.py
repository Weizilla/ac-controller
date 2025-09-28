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
