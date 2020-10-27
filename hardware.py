from gpiozero import DigitalInputDevice
from gpiozero import Button
from gpiozero import DigitalOutputDevice

refund_relay = DigitalOutputDevice(pin=17)
collect_relay = DigitalOutputDevice(pin=27)

nickel_switch = Button(pin=1, bounce_time=0.1)
dime_switch = Button(pin=7, bounce_time=0.1)
quarter_switch = Button(pin=8, bounce_time=0.1)

volume_button = DigitalInputDevice(pin=4, pull_up=True, bounce_time=0.1)
hook_switch = DigitalInputDevice(pin=18, pull_up=True, bounce_time=0.1)


def is_off_hook():
    return hook_switch.is_active
