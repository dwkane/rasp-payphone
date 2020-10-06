from hardware import collect_relay
from hardware import refund_relay
import time


def collect():
    collect_relay.on()
    time.sleep(0.6)
    collect_relay.off()


def refund():
    refund_relay.on()
    time.sleep(0.6)
    refund_relay.off()
