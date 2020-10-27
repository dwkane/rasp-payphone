from hardware import *
import time
import keypad_controller
import tone_generator
from modules.linphone import Wrapper
import modules.google.tts.tts as tts
import coin_controller as coin
from threading import Timer
from modules.linphone.number_validator import *


pressed_key_string = ""
tts = tts.TTS()
call_delay = 3000
call_attempt = False
amount_needed = 0.25
key_timer = None

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
    if is_off_hook() is True:
        tone_generator.stop_tone()
        if key_timer is not None:
            key_timer.cancel()
        if call_attempt is False:
            new_key_timer()
            key_timer.start()


def make_call():
    global pressed_key_string
    global call_attempt
    global amount_needed
    call_attempt = True
    if key_timer is not None:
        key_timer.cancel()
    # tts.say("Now dialing: " + format_number(pressed_key_string))
    # time.sleep(2)
    if is_number_valid(pressed_key_string):
        while not coin.is_enough_deposited(amount_needed):
            if call_attempt is True:
                tone_generator.play_error_tone()
                tts.say("If you would like to make a call, please deposit $" +
                        str(round(amount_needed - coin.get_coin_total(), 2)))
                time.sleep(3)
            else:
                return
        pressed_key_string = format_number(pressed_key_string)
        print("Dialing: " + pressed_key_string)
        SipClient.SipCall(pressed_key_string)
        # time.sleep(10)
        # print("Call connected: " + str(SipClient.is_call_connected()))
        coin.reset_coin_total()
    else:
        while call_attempt is True:
            tone_generator.play_error_tone()
            tts.say("We're sorry.  The number you entered cannot be completed as dialed.  "
                    "Please hang up and try your call again")
            time.sleep(3)


def new_key_timer():
    global key_timer
    key_timer = Timer(3.0, make_call)


def off_hook():
    print("Off Hook...")
    tone_generator.play_dial_tone()


def on_hook():
    global pressed_key_string
    global call_attempt
    pressed_key_string = ""
    call_attempt = False
    tone_generator.stop_tone()
    coin.reset_coin_total()
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
