import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)
inPin = 40
GPIO.setup(inPin, GPIO.IN)
realVal = GPIO.input(inPin)
print(realVal)
GPIO.cleanup()