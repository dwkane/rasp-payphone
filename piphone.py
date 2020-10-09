import coin_controller as coin
from hardware import *
import time
from pad4pi import rpi_gpio
import tone_generator

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
    # global pressed_key_string
    # pressed_key_string = str(digit)
    print(digit)
    if is_off_hook() is True:
        tone_generator.stop_tone()
        tone_generator.play_digit(digit)
        time.sleep(0.2)
        tone_generator.stop_tone()


def off_hook():
    tone_generator.play_dial_tone()


def on_hook():
    tone_generator.stop_tone()


hook_switch.when_activated = off_hook
hook_switch.when_deactivated = on_hook


keypad_init()
while True:
    time.sleep(1)
