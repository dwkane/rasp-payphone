from gpiozero import DigitalInputDevice
from gpiozero import Button
from gpiozero import DigitalOutputDevice

refund_relay = DigitalOutputDevice(pin=17)
collect_relay = DigitalOutputDevice(pin=27)

# TODO: Fix coin detection
nickel_switch = Button(pin=1, pull_up=None, active_state=False, bounce_time=0.1)
quarter_switch = Button(pin=8, pull_up=None, active_state=False, bounce_time=0.1)
dime_switch = Button(pin=7, pull_up=None, active_state=False, bounce_time=0.1)

volume_button = DigitalInputDevice(pin=4, pull_up=True, bounce_time=0.1)
hook_switch = DigitalInputDevice(pin=18, pull_up=True, bounce_time=0.1)


def is_off_hook():
    return hook_switch.is_active
