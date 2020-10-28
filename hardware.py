from gpiozero import DigitalInputDevice
from gpiozero import DigitalOutputDevice
import RPi.GPIO as GPIO
from coin_controller import coin_inserted

refund_relay = DigitalOutputDevice(pin=17)
collect_relay = DigitalOutputDevice(pin=27)

nickel = 1
dime = 7
quarter = 8

GPIO.setup(nickel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dime, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(quarter, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(nickel, GPIO.FALLING, callback=coin_inserted, bouncetime=50)
GPIO.add_event_detect(dime, GPIO.FALLING, callback=coin_inserted, bouncetime=50)
GPIO.add_event_detect(quarter, GPIO.FALLING, callback=coin_inserted, bouncetime=50)

volume_button = DigitalInputDevice(pin=4, pull_up=True, bounce_time=0.1)
hook_switch = DigitalInputDevice(pin=18, pull_up=True, bounce_time=0.1)


def is_off_hook():
    return hook_switch.is_active
