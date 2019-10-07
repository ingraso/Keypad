"""Module for keypad."""
from inspect import isfunction


def signal_is_digit(signal):
    """Return if signal is digit 0-9."""
    return 48 <= ord(signal) <= 57


def signal_is_whatever(signal):
    """Return True no matter what signal."""
    return True


# defines symbols
ALL_SYMBOLS = signal_is_whatever
ALL_DIGITS = signal_is_digit
STAR = "*"
Y = "Y"
HASHTAG = "#"


class FSM(object):
    """Class for the finite state machine."""

    def __init__(self, agent):
        # creates all rule objects for the FSM
        self.r_1 = Rule("init", ALL_SYMBOLS, "read", agent.reset_cps)
        self.r_2 = Rule("read", STAR, "verify", agent.verify_login)
        self.r_3 = Rule("read", ALL_SYMBOLS, "read", agent.append_next_password_digit)
        self.r_4 = Rule("verify", Y, "active", agent.dummy)
        self.r_5 = Rule("verify", ALL_SYMBOLS, "init", agent.dummy)
        self.r_6 = Rule("active", STAR, "read2", agent.reset_cps)
        self.r_7 = Rule("led", STAR, "time", agent.dummy)
        self.r_8 = Rule("led", HASHTAG, "logout", agent.dummy)
        self.r_9 = Rule("led", ALL_SYMBOLS, "active", agent.reset_led)
        self.r10 = Rule("time", HASHTAG, "logout", agent.dummy)
        self.r11 = Rule("time", ALL_DIGITS, "time", agent.change_ldur)
        self.r12 = Rule("time", STAR, "active", agent.change_ldur)
        self.r13 = Rule("active", ALL_SYMBOLS, "active", agent.dummy)
        self.r14 = Rule("read2", HASHTAG, "logout", agent.dummy)
        self.r15 = Rule("read2", ALL_DIGITS, "read2", agent.append_next_password_digit)
        self.r16 = Rule("read2", STAR, "verify2", agent.validate_password_change)
        self.r17 = Rule("verify2", HASHTAG, "logout", agent.dummy)
        self.r18 = Rule("verify2", Y, "active", agent.ok_format)
        self.r19 = Rule("verify2", ALL_SYMBOLS, "active", agent.wrong_format)
        self.r20 = Rule("active", HASHTAG, "logout", agent.dummy)
        self.r21 = Rule("logout", HASHTAG, "done", agent.exit_action)
        self.r22 = Rule("logout", ALL_SYMBOLS, "active", agent.dummy)

        self.rules = [
            self.r_1,
            self.r_2,
            self.r_3,
            self.r_4,
            self.r_5,
            self.r_6,
            self.r_7,
            self.r_8,
            self.r_9,
            self.r10,
            self.r11,
            self.r12,
            self.r13,
            self.r14,
            self.r15,
            self.r16,
            self.r17,
            self.r18,
            self.r19,
            self.r20,
            self.r21,
            self.r22]

        self.agent = agent

        self.current_state = "init"
        self.current_signal = None

    def add_rule(self, rule):
        """Add a new rule to the end of the FSM's rule list."""
        self.rules.append(rule)

    def get_next_signal(self):
        """Query the agent for the next signal."""
        self.current_signal = self.agent.get_next_signal()

    def run_rules(self):
        """Go through the rule set, in order, applying each rule until one of the rules is fired."""
        for rule in self.rules:
            is_fired = self.apply_rule(rule)
            if is_fired:
                return

    def apply_rule(self, rule):
        """Check whether the conditions of a rule are met and fire rule if they are."""
        if rule.match(self.current_state, self.current_signal):
            self.fire_rule(rule)
            return True
        return False

    def fire_rule(self, rule):
        """Use the consequent of a rule to set the next state of the FSM and
        call the appropriate agent action."""
        self.current_state = rule.state2
        self.agent.do_action(rule.action, self.current_signal)
        rule.action(self.current_signal)

    def main_loop(self):
        """Begin in the FSM's default state and then repeatedly call get_next_signal
        and run_rules until the FSM        enters its default final state """
        while self.current_state != "done":
            self.get_next_signal()
            self.run_rules()
        # shutdown agent, keypad, LED board??


class Rule(object):
    """Class for rule objects."""

    def __init__(self, state1, signal, state2, action):
        # triggering state of the FSM
        self.state1 = state1

        # new state of the FSM if this rule fires. Should never be a function,
        # but a symbol specifying a single, legal state of the FSM
        self.state2 = state2

        # triggering signal
        self.signal = signal  # expressed as "symbol" in the instructions?

        # the agent will be instructed to perform this action if this rule fires
        # should be a specific method that the agent object understands
        self.action = action

    def match(self, current_state, current_signal):
        """Return whether the rule applies."""
        if current_state != self.state1:
            return False

        if isfunction(self.signal):
            return self.signal(current_signal)

        return current_signal == self.signal
