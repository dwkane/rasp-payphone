import coin_controller as coin
from hardware import *
import time
import keypad_controller
import tone_generator

pressed_key_string = ""
keypad = keypad_controller.Keypad


def keypad_init():
    global keypad
    # factory = keypad_controller.KeypadFactory()
    keypad = keypad_controller.KeypadFactory().create_keypad()
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
