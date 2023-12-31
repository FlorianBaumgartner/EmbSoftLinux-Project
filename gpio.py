import RPi.GPIO as GPIO
import threading
import time

LED_RED = 16
LED_GREEN = 20
LED_BLUE = 21

BUTTON_CENTER = 26
BUTTON_UP = 6
BUTTON_DOWN = 5
BUTTON_LEFT = 19
BUTTON_RIGHT = 13


class Gpio:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(BUTTON_CENTER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUTTON_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(LED_RED, GPIO.OUT)
        GPIO.setup(LED_GREEN, GPIO.OUT)
        GPIO.setup(LED_BLUE, GPIO.OUT)

        self.thread = None
        self.running = False
        self.blinkState = False

    def __del__(self):
        GPIO.cleanup()

    def start(self):
        self.running = True
        self.setLedRed(False)
        self.setLedGreen(False)
        self.setLedBlue(False)
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def stop(self):
        self.running = False

    def _run(self):
        while self.running:
            if(self.blinkState):
                self.setLedBlue(time.time() % 0.4 > 0.2)
            else:
                self.setLedBlue(False)
            time.sleep(0.05)

    def setBlinking(self, state):
        self.blinkState = state

    def getButtonCenter(self):
        return GPIO.input(BUTTON_CENTER) == False
    
    def getButtonUp(self):
        return GPIO.input(BUTTON_UP) == False

    def getButtonDown(self):
        return GPIO.input(BUTTON_DOWN) == False
    
    def getButtonLeft(self):
        return GPIO.input(BUTTON_LEFT) == False
    
    def getButtonRight(self):
        return GPIO.input(BUTTON_RIGHT) == False
    
    def setLedRed(self, state):
        GPIO.output(LED_RED, state)

    def setLedGreen(self, state):
        GPIO.output(LED_GREEN, state)

    def setLedBlue(self, state):
        GPIO.output(LED_BLUE, state)


if __name__ == "__main__":
    gpio = Gpio()
    while True:
        gpio.setLedRed(gpio.getButtonCenter())
        gpio.setLedGreen(gpio.getButtonUp())
        gpio.setLedBlue(gpio.getButtonDown())
