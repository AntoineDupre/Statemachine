import unittest
from statemachine import StateMachine
from statemachine import StateMachineManager
from mock import MagicMock
from time import sleep


class StateMachineManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.mock = MagicMock()
        self.manager = StateMachineManager(loop_time=0.1,
                                           state_machine_cls=self.mock,
                                           arg = "Arg")
    def test_looping(self):
        self.mock.return_value = self.mock
        self.mock.finished = False
        self.manager.start()
        self.mock.assert_called_once_with(arg="Arg")
        self.assertEqual(self.manager.is_running(), True)
        self.assertEqual(self.manager.running_thread.is_alive(), True)
        self.manager.pause()
        self.assertEqual(self.manager.is_running(), False)
        self.manager.resume()
        self.assertEqual(self.manager.is_running(), True)
        self.manager.stop()




