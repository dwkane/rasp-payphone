from hardware import *
import time
import keypad_controller
import tone_generator
from modules.linphone import Wrapper
import modules.google.tts.tts as tts
import coin_controller as coin

pressed_key_string = ""
tts = tts.TTS()
call_delay = 3000
last_key_press_time = 0
call_attempt = False
amount_needed = 0.25

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
    global last_key_press_time
    if is_off_hook() is True:
        tone_generator.stop_tone()
        last_key_press_time = time.time() * 1000


def make_call():
    global pressed_key_string
    global call_attempt
    global amount_needed
    global last_key_press_time
    call_attempt = True
    currTime = time.time() * 1000
    print("currTime: " + str(currTime) + " - compare: " + str(last_key_press_time + call_delay) +
          " - last_press: " + str(last_key_press_time) + " - delay: " + str(call_delay))
    if currTime > last_key_press_time + call_delay:
        while not coin.is_enough_deposited(amount_needed):
            if is_off_hook() is True:
                tone_generator.play_error_tone()
                tts.say("If you would like to make a call, please deposit $" + str(amount_needed - coin.get_coin_total()))
                time.sleep(3)
        print("Dialing: " + pressed_key_string)
        SipClient.SipCall(pressed_key_string)


def off_hook():
    print("Off Hook...")
    tone_generator.play_dial_tone()


def on_hook():
    global pressed_key_string
    global call_attempt
    pressed_key_string = ""
    call_attempt = False
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
