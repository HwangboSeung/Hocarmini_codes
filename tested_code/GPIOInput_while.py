import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)
inPin = 40
GPIO.setup(inPin, GPIO.IN)
try:
    while True:
        realVal = GPIO.input(inPin)
        print(realVal)
        sleep(1)
except KeyboardInterrupt:
    print("Ctrl key is pressed")
    GPIO.cleanup()