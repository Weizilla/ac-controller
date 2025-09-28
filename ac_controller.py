import logging
import time
from enum import Enum

from device import Device

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

SLEEP_INTERVAL = 10 * 60
HIGH_TEMP_THRESHOLD = 80
LOW_TEMP_THRESHOLD = 75

class Action(Enum):
    TURN_ON = "on"
    TURN_OFF = "off"
    NO_OP = "no_op"

class ACController(object):
    def __init__(self, device: Device):
        self.device = device
        self.last_check = None

    def get_action(self) -> Action:
        value = self.device.value()
        temp = self.device.temperature()

        action = Action.NO_OP
        if value == 1 and temp <= LOW_TEMP_THRESHOLD:
            action = Action.TURN_OFF
        elif value == 0 and temp >= HIGH_TEMP_THRESHOLD:
            action = Action.TURN_ON

        logger.info(f"value: {value} temp: {temp} action: {action}")

        return action

    def run_once(self):
        action = self.get_action()

        if action == Action.TURN_ON:
            self.device.on()
        elif action == Action.TURN_OFF:
            self.device.off()

    def run_loop(self):
        while True:
            self.run_once()
            time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    from pi_device import PiDevice

    logger.info("Starting...")
    controller = ACController(PiDevice())
    controller.run_loop()
