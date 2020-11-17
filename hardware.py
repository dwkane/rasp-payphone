from gpiozero import DigitalInputDevice
from gpiozero import DigitalOutputDevice
import RPi.GPIO as GPIO
from coin_controller import coin_inserted
from coin_controller import vol_button_pressed

# Pin Numbers
refund_relay_pin = 17
collect_relay_pin = 27
ringer_relay_pin = 22
nickel_pin = 1
quarter_pin = 8
dime_pin = 7
volume_button_pin = 4
hook_switch_pin = 18

refund_relay = DigitalOutputDevice(pin=refund_relay_pin)
collect_relay = DigitalOutputDevice(pin=collect_relay_pin)
ringer_relay = DigitalOutputDevice(pin=ringer_relay_pin)
volume_button = DigitalInputDevice(pin=volume_button_pin, pull_up=True, bounce_time=0.05)
volume_button.when_activated = vol_button_pressed
hook_switch = DigitalInputDevice(pin=hook_switch_pin, pull_up=True, bounce_time=0.05)

# The coin switches need to be more sensitive because they only activate for a fraction of a second when a coin falls.
# Setting them up this way allows more sensitive activation by detecting a Falling Edge
GPIO.setup(nickel_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dime_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(quarter_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(nickel_pin, GPIO.FALLING, callback=coin_inserted, bouncetime=50)
GPIO.add_event_detect(dime_pin, GPIO.FALLING, callback=coin_inserted, bouncetime=50)
GPIO.add_event_detect(quarter_pin, GPIO.FALLING, callback=coin_inserted, bouncetime=50)


def is_off_hook():
    return hook_switch.is_active
