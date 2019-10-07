"""This module will contain the KPC agent and its methods"""
import keypad as kp
import led_board as lb


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
        self.path_name = 'SKRIV INN HELE HELE PATH-NAVNET TIL HVOR PASSORDET ER LAGRET HER'
        self.override_signal = None
        self.Lid = None
        self.Ldur = 0

    def init_passcode_entry(self):
        """Makes the KPC ready to start"""
        self.current_password_sequence = ''
        self.LED_board.power_up()

    def get_next_signal(self):
        """Returns the next signal"""
        if self.override_signal is not None:
            sending_signal = self.override_signal
            self.override_signal = None
            return sending_signal
        return self.keypad.get_next_signal()

    def append_next_password_digit(self):
        """To append a new digit to the current_password_sequence"""
        self.current_password_sequence += self.get_next_signal()

    def change_lid(self):
        """Change the Lid"""
        if self.validate_lid():
            self.Lid = self.current_new_lid

    def change_ldur(self):
        """Change Ldur"""
        if self.validate_ldur():
            self.Ldur = self.current_new_ldur

    def reset_agent(self):
        """To reset the password if it is typed wrong"""
        self.current_password_sequence = ''

    def verify_login(self):
        """Checks if the password is correct, and acts from that"""
        f = open(self.path_name, "r")
        password = f.read()
        if password == self.current_password_sequence:
            self.override_signal = 'Y'
            self.twinkle_leds()
        else:
            self.override_signal = 'N'
            self.flash_leds()
        f.close()

    def validate_passcode_change(self):
        """Checks if the new password is legal, and acts on that"""
        if len(self.current_new_password) >= 4 and \
                self.current_new_password.isdigit():
            f = open(self.path_name, "w")
            f.write(self.current_new_password)
            f.close()
            # Kjør lys-show for akseptert passord !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        else:
            # Kjør lys-show for feil passord !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            i = 1  # So it will stop complaining

    def validate_lid(self):
        """Checks if the chosen LED is a valid number"""
        return 0 <= self.current_new_lid < 6

    def validate_ldur(self):
        """Checks if the chosen Ldur is a valid """
        return self.current_new_ldur.isdigit()

    def light_one_led(self):
        """To light one given LED for a given amount of time"""
        self.LED_board.light_led(self.Lid, self.Ldur)

    def flash_leds(self):
        """Ask to flash all the LEDs"""
        self.LED_board.flash_all_leds(0.5)

    def twinkle_leds(self):
        """Ask to twinkle all LEDs"""
        self.LED_board.twinkle_all_leds(0.3)

    def exit_action(self):
        """Start the power_down light sequence"""
        self.LED_board.power_down()


agent = KPC()


def main():
    # A little bit confused, but somehow we must run the program
    # so that it is constantly looking for a new signal
    while True:
        print(agent.get_next_signal())
