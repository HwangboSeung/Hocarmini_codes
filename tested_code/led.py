#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)  # GPIO.BOARD
GPIO.setup(17, GPIO.OUT)

while(True):
    GPIO.output(17, False)  # HIGH
    time.sleep(2)
    GPIO.output(17, True)  # LOW
    time.sleep(2.0)
