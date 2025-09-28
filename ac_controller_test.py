import logging
import unittest
from datetime import datetime, timedelta
from freezegun import freeze_time
from unittest.mock import Mock

from ac_controller import ACController, Action, CHECK_INTERVAL

logging.disable()


class MyTestCase(unittest.TestCase):
    device = Mock()

    param_list = [
        # current value, temperature, expected action
        (1, 50, Action.TURN_OFF),
        (1, 77, Action.NO_OP),
        (1, 90, Action.NO_OP),
        (0, 50, Action.NO_OP),
        (0, 77, Action.NO_OP),
        (0, 90, Action.TURN_ON),
    ]

    def setUp(self):
        self.controller = ACController(self.device)

    def test_action(self):
        for value, temp, expected in self.param_list:
            self.device.value = Mock(return_value=value)
            self.device.temperature = Mock(return_value=temp)

            actual = self.controller.get_action()
            self.assertEqual(actual, expected, f"value: {value}, temp: {temp}, actual: {actual}, expected: {expected}")

    def test_run_once_action(self):
        self.controller.get_action = Mock(return_value=Action.NO_OP)
        self.controller.run_once()

        self.controller.get_action.assert_called_once()

    def test_run_once_no_repeated_action(self):
        self.controller.get_action = Mock(return_value=Action.NO_OP)
        self.controller.run_once()
        self.controller.run_once()
        self.controller.run_once()
        self.controller.run_once()

        self.controller.get_action.assert_called_once()

    def test_run_once_action_after_check_interval(self):
        now = datetime.now()

        with freeze_time(now) as frozen_time:
            self.controller.get_action = Mock(return_value=Action.NO_OP)
            self.controller.run_once()

            self.controller.get_action.assert_called_once()

            new_now = now + timedelta(milliseconds=CHECK_INTERVAL + 1000)
            frozen_time.move_to(new_now)

            self.controller.run_once()

            call_count = self.controller.get_action.call_count
            self.assertEqual(call_count, 2)



if __name__ == '__main__':
    unittest.main()
