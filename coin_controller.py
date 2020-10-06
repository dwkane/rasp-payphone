from hardware import collect_relay
from hardware import refund_relay
import time

amount_inserted = 0.00


def collect():
    collect_relay.on()
    time.sleep(0.6)
    collect_relay.off()


def refund():
    refund_relay.on()
    time.sleep(0.6)
    refund_relay.off()


def reset_amount():
    global amount_inserted
    amount_inserted = 0.00


def return_amount():
    return amount_inserted


def quarter():
    global amount_inserted
    amount_inserted += 0.25
