from gpiozero import DigitalInputDevice
from gpiozero import DigitalOutputDevice

refund_relay = DigitalOutputDevice(17)
collect_relay = DigitalOutputDevice(27)

nickel_switch = DigitalInputDevice(1, pull_up=True, bounce_time=0.1)
dime_switch = DigitalInputDevice(7, pull_up=True, bounce_time=0.1)
quarter_switch = DigitalInputDevice(8, pull_up=True, bounce_time=0.1)

volume_button = DigitalInputDevice(4, pull_up=True, bounce_time=0.1)
hook_switch = DigitalInputDevice(18, pull_up=True, bounce_time=0.1)


def is_off_hook():
    return hook_switch.is_active
