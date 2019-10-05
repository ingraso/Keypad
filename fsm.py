"""Module for keypad."""
from inspect import isfunction

def signal_is_digit(signal):
    """Return if signal is digit 0-9"""
    return 48 <= ord(signal) <= 57


class FSM:
    """Class for the finite state machine."""

    def __init__(self, agent):
        self.agent = agent
        self.rule_list = []
        self.next_signal = None
        # self.current_password = "" # will be sent to agent
        # self.cumul_password = ""  # will be sent to agent
        self.current_state = None

    def add_rule(self, rule):
        """Add a new rule to the end of the FSM's rule list."""
        self.rule_list.append(rule)

    def get_next_signal(self):
        """Query the agent for the next signal."""
        self.next_signal = self.agent.get_next_signal()

    def run_rules(self):
        """Go through the rule set, in order, applying each rule until one of the rules is fired."""
        for rule in self.rule_list:
            k = 0  # FIXX!!

    def apply_rule(self, rule):
        """Check whether the conditions of a rule are met."""
        # checks if the internal state of the FSM matches the rule
        k = 0
        # FIX!


class Rule:
    """Class for rule objects."""

    def __init__(self, state1, state2, signal, action):
        # triggering state of the FSM
        self.state1 = state1

        # new state of the FSM if this rule fires. Should never be a function,
        # but a symbol specifying a single, legal state of the FSM
        self.state2 = state2

        # triggering signal
        self.signal = signal    # expressed as "symbol" in the instructions?

        # the agent will be instructed to perform this action if this rule fires
        # should be a specific method that the agent object understands
        self.action = action
