import coin_controller as coin
from hardware import *
import time
import keypad_controller
import tone_generator

pressed_key_string = ""


def keypad_init():
    k_pad = keypad_controller.KeypadFactory().create_keypad()
    k_pad.registerKeyPressHandler(keypad_pressed)
    k_pad.registerKeyReleaseHandler(keypad_released)
    return k_pad


def keypad_pressed(digit):
    global pressed_key_string
    if is_off_hook() is True:
        pressed_key_string = pressed_key_string + str(digit)
        tone_generator.stop_tone()
        tone_generator.play_digit(digit)


def keypad_released():
    global pressed_key_string
    tone_generator.stop_tone()
    if len(pressed_key_string) >= 11:
        print(pressed_key_string)


def off_hook():
    tone_generator.play_dial_tone()


def on_hook():
    global pressed_key_string
    pressed_key_string = ""
    tone_generator.stop_tone()


hook_switch.when_activated = off_hook
hook_switch.when_deactivated = on_hook


keypad = keypad_init()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Bye")
