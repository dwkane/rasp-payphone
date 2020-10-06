import coin_controller as coin
import hardware
import time
# from signal import pause

# coin.refund()
# time.sleep(2)
# coin.collect()


def keypad_pressed(digit):
	print(digit)


hardware.quarter_switch.when_pressed = coin.quarter


while True:
	time.sleep(0.1)
	print(coin.return_amount())
