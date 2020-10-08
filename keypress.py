from pad4pi import rpi_gpio

KEYPAD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    ["*", 0, "#"]
]

ROW_PINS = [21, 20, 16, 12]  # BCM numbering
COL_PINS = [25, 24, 23]  # BCM numbering

factory = rpi_gpio.KeypadFactory()

# Try factory.create_4_by_3_keypad
# and factory.create_4_by_4_keypad for reasonable defaults
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)


def print_key(key):
    print(key)


# printKey will be called each time a keypad button is pressed
keypad.registerKeyPressHandler(print_key)
i = input('')
keypad.cleanup()
