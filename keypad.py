"""This module will contain the KeyPad-object"""
from time import sleep
import RPi.GPIO as GPIO


def setup():
    """This method will set the proper mode via GPIO.setmode(GPIO.BCM).
    It will also set the row-pins as output and the column-pins as input."""
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    print("now we have set pin 18 to OUT")
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


class KeyPad:
    """This class is representing the keypad, but I am currently
     not sure what happens here"""

    def __init__(self):
        """This class initializes the KeyPad-object,
        so the setup-method must be called"""
        setup()
        # A dict that uses a tupple with (row, col) as key
        self.signs = {(18, 17): '1', (18, 27): '2', (18, 22): '3',
                      (23, 17): '4', (23, 27): '5', (23, 22): '6',
                      (24, 17): '7', (24, 27): '8', (24, 22): '9',
                      (25, 17): '*', (25, 27): '0', (25, 22): '#'}

    def do_polling(self):
        """Will use nested loops to determine which key is currently being pressed.
        We will check if a key is pressed 10 times with 10ms sleep-time."""
        row_pins = [18, 23, 24, 25]
        col_pins = [17, 27, 22]

        for row in row_pins:
            # Set the current row_pin HIGH
            GPIO.output(row, GPIO.HIGH)
            for col in col_pins:
                # If both col and row is high (10 times), save the values in a
                # tupple that will also be stored in a dict
                i = 0
                for j in range(0, 10):
                    if GPIO.input(col) == GPIO.HIGH:
                        i += 1
                    sleep(0.05)
                if i == 10:
                    tupple_answer = (row, col)
                    # print("i ble 10 og tuppelen er:", tupple_answer)
                    return self.signs[tupple_answer]
            GPIO.output(row, GPIO.LOW)
        return None

    def get_next_signal(self):
        """The interface between the agent and the keypad.
        Calls do_polling until a key press is detected."""
        next_signal = None
        while next_signal is None:
            next_signal = self.do_polling()
            sleep(0.5)
        return next_signal
