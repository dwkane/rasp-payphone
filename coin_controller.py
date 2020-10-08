from hardware import *
import time
from signal import pause


coin_total = 0.00


def collect():
    collect_relay.on()
    time.sleep(0.6)
    collect_relay.off()


def refund():
    refund_relay.on()
    time.sleep(0.6)
    refund_relay.off()


def reset_coin_total():
    global coin_total
    coin_total = 0.00


def get_coin_total():
    return round(coin_total, 2)


def coin_inserted(switch):
    global coin_total
    if switch is quarter_switch:
        coin_total += 0.25
    elif switch is dime_switch:
        coin_total += 0.10
    elif switch is nickel_switch:
        coin_total += 0.05


quarter_switch.when_activated = coin_inserted
dime_switch.when_activated = coin_inserted
nickel_switch.when_activated = coin_inserted

