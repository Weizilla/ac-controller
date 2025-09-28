import logging
import unittest
from unittest.mock import Mock

from ac_controller import ACController, Action

logging.disable()


class MyTestCase(unittest.TestCase):
    device = Mock()
    controller = ACController(device)

    param_list = [
        # current value, temperature, expected action
        (1, 50, Action.TURN_OFF),
        (1, 77, Action.NO_OP),
        (1, 90, Action.NO_OP),
        (0, 50, Action.NO_OP),
        (0, 77, Action.NO_OP),
        (0, 90, Action.TURN_ON),
    ]

    def test_action(self):

        for value, temp, expected in self.param_list:
            self.device.value = Mock(return_value=value)
            self.device.temperature = Mock(return_value=temp)

            actual = self.controller.get_action()
            self.assertEqual(actual, expected, f"value: {value}, temp: {temp}, actual: {actual}, expected: {expected}")


if __name__ == '__main__':
    unittest.main()
