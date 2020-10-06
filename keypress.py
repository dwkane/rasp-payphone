import time
from keypad import KeyPad
import piphone

kp = KeyPad()

while True:
	digit = None
	while digit is None:
		digit = kp.get_key()
	time.sleep(0.2)
	piphone.keypad_pressed(digit)
