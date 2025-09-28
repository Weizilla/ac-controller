from datetime import datetime, timedelta
import logging
import time
from enum import Enum

from device import Device

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

SLEEP_INTERVAL = 10 * 60 * 1000
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
        self.next_run = None

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

    def run_loop(self):
        while True:
            self.run_once()
            time.sleep(SLEEP_INTERVAL)

    def run_once(self):
        action = self.get_action()
        self.last_check = datetime.now()
        self.next_run = datetime.now() + timedelta(milliseconds=SLEEP_INTERVAL)

        if action == Action.TURN_ON:
            self._turn_on()
        elif action == Action.TURN_OFF:
            self._turn_off()

        self._update_message()

    def _turn_on(self):
        self.device.on()

    def _turn_off(self):
        self.device.off()

    def _update_message(self):
        status = "ON " if self.device.value() else "OFF"
        temp = self.device.temperature()
        time = self.last_check.strftime("%I:%M:%S %p") if self.last_check else "NO TIME"
        next_run_mins = int((self.next_run - datetime.now()).total_seconds() / 60)

        line_1 = f"{status}           {temp}"
        line_2 = f"{time}   {next_run_mins}"

        self.device.set_lcd_message(line_1, line_2)

        color = [0, 100, 0] if self.device.value() else [100, 0, 0]
        self.device.set_lcd_color(color)


if __name__ == "__main__":
    from pi_device import PiDevice

    logger.info("Starting...")
    controller = ACController(PiDevice())
    controller.run_loop()
