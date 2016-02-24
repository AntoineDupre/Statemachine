State Machine
=============

Provide 2 classes : StateMachine , StateMachineManager

StateMachine
------------

Class for inheritance  

```
class MyStateMachine(StateMachine):
```

Define state as list of str in the __init__ method:

```

    states = ["INIT",
              "STEP_01",
              "STEP_02"
              "DONE"]
    StateMachine.__init__(self, states)
```

   
Then describe actions and transitions : 


```

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
```


StateMachineManager
-------------------
Thread manager to run state machine
args :

- loop time : time between loop execution
- state_machine_cls : class of the state machine
- state_machine_kwargs:  arguments of the state machine

This manager call in a thread self.state_machine.proceed periodically.
It offer a interface to :

- start : run the state machine proceed loop at "loop_time" rate
- stop : stop state machine loop. Use start to run it again (from the beginning)
- pause: break state machine proceed loop
- resume: start state machine proceed loop in the current state
- next_step: only one loop iteration and then pause