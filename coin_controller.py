import hardware
import time


coin_total = 0


def collect():
    reset_coin_total()
    hardware.collect_relay.on()
    time.sleep(0.6)
    hardware.collect_relay.off()


def refund():
    reset_coin_total()
    hardware.refund_relay.on()
    time.sleep(0.6)
    hardware.refund_relay.off()


def reset_coin_total():
    global coin_total
    coin_total = 0


def get_coin_total():
    return coin_total / 100


def is_enough_deposited(needed):
    if needed > round(get_coin_total(), 2):
        return False
    else:
        return True


def coin_inserted(switch):
    global coin_total
    if switch is hardware.quarter_switch:
        coin_total += 25
    elif switch is hardware.dime_switch:
        coin_total += 10
    elif switch is hardware.nickel_switch:
        coin_total += 5
    print(get_coin_total())


hardware.dime_switch.when_pressed = coin_inserted
hardware.nickel_switch.when_pressed = coin_inserted
hardware.quarter_switch.when_pressed = coin_inserted
