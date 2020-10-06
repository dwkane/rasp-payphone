import coin_controller as coin
import time
import keypad

# coin.refund()
# time.sleep(2)
# coin.collect()

kp = keypad.KeyPad()


while True:
	digit = None
	while digit is None:
		digit = kp.get_key()
	print(digit)
	time.sleep(0.2)
