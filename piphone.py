import coin_controller as coin
from hardware import *
import time
import keypad_controller
import tone_generator
from linphone import Wrapper

pressed_key_string = ""


SipClient = Wrapper.Wrapper()
SipClient.StartLinphone()
# SipClient.SipRegister(username="281329", password="24KeeJGK3cVWkw#", hostname="seattle2.voip.ms")
# SipClient.RegisterCallbacks(OnIncomingCall=OnIncomingCall, OnOutgoingCall=OnOutgoingCall,
# OnRemoteHungupCall=OnRemoteHungupCall, OnSelfHungupCall=OnSelfHungupCall)
SipClient.start()


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
        print("Dialing: " + pressed_key_string)
        SipClient.SipCall(pressed_key_string)
        pressed_key_string = ""


def off_hook():
    print("Off Hook...")
    tone_generator.play_dial_tone()
    # SipClient.SipCall("18002553700")


def on_hook():
    global pressed_key_string
    pressed_key_string = ""
    tone_generator.stop_tone()
    if SipClient is not None:
        print("Hanging Up...")
        SipClient.SipHangup()


hook_switch.when_activated = off_hook
hook_switch.when_deactivated = on_hook
keypad = keypad_init()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Bye")
