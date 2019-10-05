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
            1: LED(13),
            2: LED(19),
            3: LED(26),
            4: LED(16),
            5: LED(20),
            6: LED(21)}

    def setup(self):
        """ set the proper mode """
        gpio.setmode(gpio.BCM)

        # have to setup the input and output pins!!
        #test branch

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
        # time_flashed is the duration the LEDs have flashed
        time_flashed = 0
        # last_state remembers the last state of the LED (1 = high, 0 = low)
        last_state = 0

        while time_flashed < sec:
            for key in self.pins:
                if last_state == 0:
                    gpio.output(self.pins[key], gpio.HIGH)
                else:
                    gpio.output(self.pins[key], gpio.LOW)

            if key == 6:
                last_state = (last_state + 1) % 2

            sleep(0.2)
            time_flashed += 0.2

    def twinkle_all_leds(self, sec):
        """ turn all LEDs on and off in sequence
            for 'sec' seconds when password is verified """
        for key in self.pins:
            gpio.output(self.pins[key], gpio.HIGH)
            sleep(sec / 6)
            gpio.output(self.pins[key], gpio.LOW)

    def power_up(self):
        """ light show on power up """
        gpio.output(self.pins[1], gpio.HIGH)
        gpio.output(self.pins[3], gpio.HIGH)
        gpio.output(self.pins[5], gpio.HIGH)
        sleep(0.5)

        gpio.output(self.pins[1], gpio.LOW)
        gpio.output(self.pins[3], gpio.LOW)
        gpio.output(self.pins[5], gpio.LOW)
        gpio.output(self.pins[2], gpio.HIGH)
        gpio.output(self.pins[4], gpio.HIGH)
        gpio.output(self.pins[6], gpio.HIGH)
        sleep(0.5)

        gpio.output(self.pins[2], gpio.LOW)
        gpio.output(self.pins[4], gpio.LOW)
        gpio.output(self.pins[6], gpio.LOW)

        gpio.output(self.pins[1], gpio.HIGH)
        sleep(0.1)

        gpio.output(self.pins[1], gpio.LOW)
        gpio.output(self.pins[2], gpio.HIGH)
        sleep(0.1)

        gpio.output(self.pins[2], gpio.LOW)
        gpio.output(self.pins[3], gpio.HIGH)
        sleep(0.1)

        gpio.output(self.pins[3], gpio.LOW)
        gpio.output(self.pins[4], gpio.HIGH)
        sleep(0.1)

        gpio.output(self.pins[4], gpio.LOW)
        gpio.output(self.pins[5], gpio.HIGH)
        sleep(0.1)

        gpio.output(self.pins[5], gpio.LOW)
        gpio.output(self.pins[6], gpio.HIGH)
        sleep(0.1)

        gpio.output(self.pins[6], gpio.LOW)

    def power_down(self):
        """ light show on power down """
        gpio.output(self.pins[2], gpio.HIGH)
        gpio.output(self.pins[4], gpio.HIGH)
        gpio.output(self.pins[6], gpio.HIGH)
        sleep(0.5)

        gpio.output(self.pins[2], gpio.LOW)
        gpio.output(self.pins[4], gpio.LOW)
        gpio.output(self.pins[6], gpio.LOW)
        gpio.output(self.pins[1], gpio.HIGH)
        gpio.output(self.pins[3], gpio.HIGH)
        gpio.output(self.pins[5], gpio.HIGH)
        sleep(0.5)

        gpio.output(self.pins[1], gpio.LOW)
        gpio.output(self.pins[3], gpio.LOW)
        gpio.output(self.pins[5], gpio.LOW)

        gpio.output(self.pins[6], gpio.HIGH)
        sleep(0.1)

        gpio.output(self.pins[6], gpio.LOW)
        gpio.output(self.pins[5], gpio.HIGH)
        sleep(0.1)

        gpio.output(self.pins[5], gpio.LOW)
        gpio.output(self.pins[4], gpio.HIGH)
        sleep(0.1)

        gpio.output(self.pins[4], gpio.LOW)
        gpio.output(self.pins[3], gpio.HIGH)
        sleep(0.1)

        gpio.output(self.pins[3], gpio.LOW)
        gpio.output(self.pins[2], gpio.HIGH)
        sleep(0.1)

        gpio.output(self.pins[2], gpio.LOW)
        gpio.output(self.pins[1], gpio.HIGH)
        sleep(0.1)

        gpio.output(self.pins[1], gpio.LOW)
