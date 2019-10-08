"""This module will contain the KPC agent and its methods"""
import keypad as kp
import led_board as lb
import fsm as f


class KPC:
    """This class is for the KPC-object, which will work as the
    connection between the other classes"""

    def __init__(self):
        """Initializing the KPC-object"""
        self.keypad = kp.KeyPad()
        self.LED_board = lb.LedBoard()
        self.current_password_sequence = ''
        self.current_new_password = ''
        self.current_new_lid = ''
        self.current_new_ldur = ''
        self.path_name = 'password.txt'
        self.override_signal = None
        self.lid = None
        self.ldur = 0

    def init_passcode_entry(self, symbol):
        """Makes the KPC ready to start"""
        self.current_password_sequence = ''
        self.LED_board.power_up()

    def reset_cps(self, symbol):
        """To reset the password if it is typed wrong"""
        self.current_password_sequence = ''

    def reset_lid(self, symbol):
        """To reset the lid to None"""
        self.lid = None

    def get_next_signal(self):
        """Returns the next signal"""
        if self.override_signal is not None:
            sending_signal = self.override_signal
            self.override_signal = None
            print("Override signal er", sending_signal)
            return sending_signal
        next_signal = self.keypad.get_next_signal()
        print("next signal er", next_signal)
        return next_signal

    def append_next_password_digit(self, symbol):
        """To append a new digit to the current_password_sequence"""
        self.current_password_sequence += symbol

    def change_lid(self, new_lid):
        """Change the Lid. The fsm will send inn the new_lid"""
        self.current_new_lid = new_lid
        self.current_new_ldur = ''
        # ^When we change the Lid, we can also reset the Ldur
        if self.validate_lid():
            self.lid = int(self.current_new_lid)

    def change_ldur(self, new_char):
        """Change Ldur"""
        print("New char er: ", new_char)
        if new_char == '*':
            print("Nå er vi i if new_char == *")
            # If the last signal in the string is a star, finish
            if self.validate_ldur():
                print("Vi er i if self.validate_ldur")
                self.ldur = int(self.current_new_ldur)
                self.light_one_led()
            else:
                print("Vi kom ikke inn i innerste if")
                self.ldur = 0
        else:
            self.current_new_ldur += new_char
            print("Vi kom ikke inn i første if")

    def verify_login(self, symbol):
        """Checks if the password is correct, and acts from that"""
        file = open(self.path_name, "r")
        password = file.read()
        if password == self.current_password_sequence:
            self.override_signal = 'Y'
            self.twinkle_leds()
        else:
            self.override_signal = 'N'
            self.flash_leds()
        file.close()

    def validate_passcode_change(self, symbol):
        """Checks if the new password is legal, and acts on that"""
        self.current_new_password = self.current_password_sequence
        if len(self.current_new_password) >= 4 and \
                self.current_new_password.isdigit():
            f = open(self.path_name, "w")
            f.write(self.current_new_password)
            f.close()
            self.override_signal = 'Y'
        else:
            self.override_signal = 'N'

    def validate_lid(self):
        """Checks if the chosen LED is a valid number"""
        return 0 <= int(self.current_new_lid) < 6

    def validate_ldur(self):
        """Checks if the chosen Ldur is a valid """
        return self.current_new_ldur.isdigit()

    def ok_format(self, symbol):
        """Will be called if the new password is accepted"""
        self.LED_board.verify_new_password()

    def wrong_format(self, symbol):
        """Will be called if the new password is wrong"""
        self.LED_board.wrong_new_password()

    def light_one_led(self):
        """To light one given LED for a given amount of time"""
        self.LED_board.light_led(self.lid, self.ldur)

    def flash_leds(self):
        """Ask to flash all the LEDs"""
        self.LED_board.flash_all_leds(2)

    def twinkle_leds(self):
        """Ask to twinkle all LEDs"""
        self.LED_board.twinkle_all_leds(2)

    def exit_action(self, symbol):
        """Start the power_down light sequence"""
        self.LED_board.power_down()

    def dummy(self, symbol):
        """This is a dummy-method"""
        return


def main():
    """Method to run program"""
    # A little bit confused, but somehow we must run the program
    # so that it is constantly looking for a new signal
    agent = KPC()
    fsm = f.FSM(agent)
    fsm.main_loop()


main()
