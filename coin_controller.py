import gpiozero
import time


def refund():
    refund_relay = gpiozero.DigitalOutputDevice(17)
    refund_relay.on()
    time.sleep(0.6)
    refund_relay.off()


def collect():
    collect_relay = gpiozero.DigitalOutputDevice(27)
    collect_relay.on()
    time.sleep(0.6)
    collect_relay.off()


# def hello_world():
#   print("It works!")
#   sleep(0.2)


# button = gpiozero.Button(23)

# button.when_pressed = hello_world

# pause()
