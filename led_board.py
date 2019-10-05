""" module for LED-board """
from time import sleep
import RPi.GPIO as gpio
from gpiozero import LED

"""
To declare a pin to input: GPIO.setup(pin, GPIO.IN)
To declare a pin to output: GPIO.setup(pin, GPIO.OUT)

To set the voltage of an output pin to high: GPIO.output(outpin, GPIO.HIGH)
To set the voltage of an output pin to low: GPIO.output(outpin, GPIO.LOW)
"""


class LedBoard:
    """ class for LED-board """

    def __init__(self):
        """ initialize """
        self.pins = {
            "led1": LED(13),
            "led2": LED(19),
            "led3": LED(26),
            "led4": LED(16),
            "led5": LED(20),
            "led6": LED(21)}

    def setup(self):
        """ set the proper mode """
        gpio.setmode(gpio.BCM)

    def light_led(self, led, sec):
        """ turn on one LED by making the
            appropriate combination of input
            and output declarations """

        # remember to find out how to get the value from the input/given key
        gpio.output(self.pins[led], gpio.HIGH)
        sleep(sec)
        gpio.output(self.pins[led], gpio.LOW)

    def flash_all_leds(self, sec):
        """ flash all LEDs on and off for
            'sec' seconds when password is wrong """

    def twinkle_all_leds(self, sec):
        """ turn all LEDs on and off in sequence
            for 'sec' seconds when password is verified """

    def power_up(self):
        """ light show on power up """

    def power_down(self):
        """ light show on power down """
