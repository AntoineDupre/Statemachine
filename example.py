from statemachine import StateMachine
from statemachine import StateMachineManager
from time import sleep

class MyStateMachine(StateMachine):
    def __init__(self, dummy):
        self.dummy = dummy
        self.count = 0
        #             ----
        #             |  |
        #             V  |
        # INIT ----> STEP_01 ----> DONE
        #             ^  |
        #             |  V
        #            STEP_02
        states = ["INIT",
                  "STEP_01",
                  "STEP_02",
                  "DONE"]
        StateMachine.__init__(self, states)
        # first state, "when" statement is evaluate at each loop tic.
        # If it return true, go to step_01
        self.INIT.when(lambda: self.dummy.is_step_finished).goto(self.STEP_01)
        # Setup an action that will be executed each time we enter in STEP_01
        # state (from another state)
        self.STEP_01.set_action(self.action_01)
        # Setup a recurring action that will be executed each time we will
        # explicitly request to go into step_01 from step_01
        # (inner state looping)
        self.STEP_01.set_recurring_action(self.action_recursive)
        # Go to next state if "when" statement is true
        self.STEP_01.when(lambda: self.dummy.is_step_finished).goto(self.DONE)
        # Execute change state machine to the current state (will execute
        # recurring action) if when statement is True
        one_to_one = lambda: not self.dummy.is_step_finished and self.count < 3
        self.STEP_01.when(one_to_one).goto(self.STEP_01)
        # If "when" statement is true, execute action 2 and change state
        one_to_two = lambda: self.dummy.is_specific_action
        self.STEP_01.when(one_to_two).do(self.action_02).goto(self.STEP_02)
        # Go to step 01 if trigger next step and execute action 03
        two_to_one = lambda: self.dummy.is_step_finished
        self.STEP_02.when(two_to_one).goto(self.STEP_01).do(self.action_03)
        # last step action
        self.DONE.set_action(self.done)

    def action_01(self):
        print "MyStateMachine {}:: Action 01 ".format(self.state)

    def action_02(self):
        print "MyStateMachine {}:: Action 02".format(self.state)

    def action_03(self):
        print "MyStateMachine {}:: Action_03".format(self.state)

    def action_recursive(self):
        print "MyStateMachine {}:: Repeated action".format(self.state)
        self.count += 1
        sleep(0.5)

    def done(self):
        print "MyStateMachine {}:: Done".format(self.state)


class MyDummy(object):
    def __init__(self):
        self.set_finished = False
        self.specific_action = False

    def trigger_specific_action(self):
        self.specific_action = True

    @property
    def is_specific_action(self):
        if self.specific_action:
            self.specific_action = False
            return True
        return False

    def trigger_next_step(self):
        self.set_finished = True

    @property
    def is_step_finished(self):
        if self.set_finished:
            self.set_finished = False
            return True
        return False


dummy = MyDummy()
manager = StateMachineManager(loop_time=3,
                              state_machine_cls=MyStateMachine,
                              dummy=dummy)

# play with manager and dummy to trigger next step
