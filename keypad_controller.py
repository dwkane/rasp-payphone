import RPi.GPIO as GPIO
import time
from threading import Timer

DEFAULT_KEY_DELAY = 100
DEFAULT_REPEAT_DELAY = 1.0
DEFAULT_REPEAT_RATE = 1.0
DEFAULT_DEBOUNCE_TIME = 10


class KeypadFactory:

    @staticmethod
    def create_keypad(keypad=None, row_pins=None, col_pins=None, key_delay=DEFAULT_KEY_DELAY, repeat=False,
                      repeat_delay=None, repeat_rate=None, gpio_mode=GPIO.BCM):

        if keypad is None:
            keypad = [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
                ["*", 0, "#"]
            ]

        if row_pins is None:
            row_pins = [21, 20, 16, 12]  # BCM numbering

        if col_pins is None:
            col_pins = [25, 24, 23]  # BCM numbering

        return Keypad(keypad, row_pins, col_pins, key_delay, repeat, repeat_delay, repeat_rate, gpio_mode)


class Keypad:
    def __init__(self, keypad, row_pins, col_pins, key_delay=DEFAULT_KEY_DELAY, repeat=False, repeat_delay=None,
                 repeat_rate=None, gpio_mode=GPIO.BCM):
        self._press_handlers = []
        self._release_handlers = []

        self._keypad = keypad
        self._row_pins = row_pins
        self._col_pins = col_pins
        self._key_delay = key_delay
        self._repeat = repeat
        self._repeat_delay = repeat_delay
        self._repeat_rate = repeat_rate
        self._repeat_timer = None
        if repeat:
            self._repeat_delay = repeat_delay if repeat_delay is not None else DEFAULT_REPEAT_DELAY
            self._repeat_rate = repeat_rate if repeat_rate is not None else DEFAULT_REPEAT_RATE
        else:
            if repeat_delay is not None:
                self._repeat = True
                self._repeat_rate = repeat_rate if repeat_rate is not None else DEFAULT_REPEAT_RATE
            elif repeat_rate is not None:
                self._repeat = True
                self._repeat_delay = repeat_delay if repeat_delay is not None else DEFAULT_REPEAT_DELAY

        self._last_key_press_time = 0
        self._first_repeat = True

        GPIO.setmode(gpio_mode)

        self._setRowsAsInput()
        self._setColumnsAsOutput()

    def registerKeyPressHandler(self, handler):
        self._press_handlers.append(handler)

    def unregisterKeyPressHandler(self, handler):
        self._press_handlers.remove(handler)

    def clearKeyPressHandlers(self):
        self._press_handlers = []

    def registerKeyReleaseHandler(self, handler):
        self._release_handlers.append(handler)

    def unregisterKeyReleaseHandler(self, handler):
        self._release_handlers.remove(handler)

    def clearKeyReleaseHandlers(self):
        self._release_handlers = []

    def _repeatTimer(self):
        self._repeat_timer = None
        self._onKeyPress(None)

    def _onKeyPress(self, pin):
        if GPIO.input(pin):
            for handler in self._release_handlers:
                handler()
            return

        currTime = self.getTimeInMillis()
        if currTime < self._last_key_press_time + self._key_delay:
            return

        keyPressed = self.getKey()
        if keyPressed is not None:
            for handler in self._press_handlers:
                handler(keyPressed)
            self._last_key_press_time = currTime
            if self._repeat:
                self._repeat_timer = Timer(self._repeat_delay if self._first_repeat else 1.0/self._repeat_rate,
                                           self._repeatTimer)
                self._first_repeat = False
                self._repeat_timer.start()
        else:
            if self._repeat_timer is not None:
                self._repeat_timer.cancel()
            self._repeat_timer = None
            self._first_repeat = True

    def _setRowsAsInput(self):
        # Set all rows as input
        for index in range(len(self._row_pins)):
            GPIO.setup(self._row_pins[index], GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(self._row_pins[index], GPIO.BOTH, callback=self._onKeyPress,
                                  bouncetime=DEFAULT_DEBOUNCE_TIME)

    def _setColumnsAsOutput(self):
        # Set all columns as output low
        for j in range(len(self._col_pins)):
            GPIO.setup(self._col_pins[j], GPIO.OUT)
            GPIO.output(self._col_pins[j], GPIO.LOW)

    def getKey(self):

        keyVal = None

        # Scan rows for pressed key
        rowVal = None
        for index in range(len(self._row_pins)):
            tmpRead = GPIO.input(self._row_pins[index])
            if tmpRead == 0:
                rowVal = index
                break

        # Scan columns for pressed key
        colVal = None
        if rowVal is not None:
            for index in range(len(self._col_pins)):
                GPIO.output(self._col_pins[index], GPIO.HIGH)
                if GPIO.input(self._row_pins[rowVal]) == GPIO.HIGH:
                    GPIO.output(self._col_pins[index], GPIO.LOW)
                    colVal = index
                    break
                GPIO.output(self._col_pins[index], GPIO.LOW)

        # Determine pressed key, if any
        if colVal is not None:
            keyVal = self._keypad[rowVal][colVal]

        return keyVal

    def cleanup(self):
        if self._repeat_timer is not None:
            self._repeat_timer.cancel()
        GPIO.cleanup()
        print("Bye")

    @staticmethod
    def getTimeInMillis():
        return time.time() * 1000
