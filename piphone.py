import coin_controller as coin
import time
from signal import pause
from pad4pi import rpi_gpio
import pygame , pygame.sndarray
import numpy
import scipy.signal

pressed_key_string = ""
keypad = rpi_gpio.Keypad


def keypad_init():
    global keypad
    KEYPAD = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        ["*", 0, "#"]
    ]

    ROW_PINS = [21, 20, 16, 12]  # BCM numbering
    COL_PINS = [25, 24, 23]  # BCM numbering

    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
    # printKey will be called each time a keypad button is pressed
    keypad.registerKeyPressHandler(keypad_pressed)


def keypad_pressed(digit):
    global pressed_key_string
    pressed_key_string = str(digit)


def square_wave(hz, peak, duty_cycle=.5, n_samples=sample_rate):
    t = numpy.linspace(0, 1, 500 * 440/hz, endpoint=False)
    wave = scipy.signal.square(2 * numpy.pi * 5 * t, duty=duty_cycle)
    wave = numpy.resize(wave, (n_samples,))
    return peak / 2 * wave.astype(numpy.int16)


def audio_freq(freq=800):
    global sound
    sample_wave = square_wave(freq, 4096)
    sound = pygame.sndarray.make_sound(sample_wave)







sample_rate = 48000
pygame.mixer.pre_init(sample_rate, -16, 1, 1024)
pygame.init()


keypad_init()
while True:
    time.sleep(1)
