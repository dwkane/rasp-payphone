import coin_controller as coin
import time
from signal import pause
from keypress import get_key_pressed


def keypad_pressed(digit):
	print(digit)


while True:
	print(get_key_pressed())
