from gpiozero import Button
from gpiozero import DigitalOutputDevice

refund_relay = DigitalOutputDevice(17)
collect_relay = DigitalOutputDevice(27)

nickel_switch = Button(1, bounce_time=0.2)
dime_switch = Button(7, bounce_time=0.2)
quarter_switch = Button(8, bounce_time=0.2)

volume_button = Button(3, bounce_time=0.2)

hook_switch = Button(12, bounce_time=0.2)
