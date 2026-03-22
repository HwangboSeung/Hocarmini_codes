import RPi.GPIO as GPIO
import time

LED_PIN = 17
PIR_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

try:
    while True:
        time.sleep(0.01)
        if GPIO.input(PIR_PIN) == GPIO.HIGH:
            GPIO.output(LED_PIN, GPIO.HIGH)
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
except KeyboardInterrupt:
    print("cleaning up GPIOs")

GPIO.cleanup()