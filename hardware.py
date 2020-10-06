import gpiozero

refund_relay = gpiozero.DigitalOutputDevice(17)
collect_relay = gpiozero.DigitalOutputDevice(27)

nickel_switch = gpiozero.DigitalInputDevice(1, pull_up=True, bounce_time=0.2)
dime_switch = gpiozero.DigitalInputDevice(7, pull_up=True, bounce_time=0.2)
quarter_switch = gpiozero.DigitalInputDevice(8, pull_up=True, bounce_time=0.2)

volume_button = gpiozero.DigitalInputDevice(3, pull_up=True, bounce_time=0.2)

hook_switch = gpiozero.DigitalInputDevice(12, pull_up=True, bounce_time=0.2)
