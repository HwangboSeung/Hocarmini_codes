import RPi.GPIO as GPIO
import time

# Setup
motor1 = 17  # Input Pin
motor2 = 18  # Input Pin
enable = 27  # Enable Pin
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setup(motor1, GPIO.OUT)
GPIO.setup(motor2, GPIO.OUT)
GPIO.setup(enable, GPIO.OUT)

# PWM
pwm = GPIO.PWM(enable, 100)  # Create PWM channel at 100 Hz frequency

def forward(speed):
    pwm.start(speed)
    GPIO.output(motor1, GPIO.HIGH)
    GPIO.output(motor2, GPIO.LOW)

def backward(speed):
    pwm.start(speed)
    GPIO.output(motor1, GPIO.LOW)
    GPIO.output(motor2, GPIO.HIGH)

def change_speed(speed):
    pwm.ChangeDutyCycle(speed)

def stop():
    pwm.stop()
    GPIO.cleanup()

# Example Usage
try:
    forward(50)  # Move forward at half speed
    time.sleep(2)  # Move for 2 seconds
    change_speed(75)  # Increase speed
    time.sleep(2)  # Move for another 2 seconds
    backward(50)  # Move backward at half speed
    time.sleep(2)  # Move for 2 seconds
    stop()  # Stop the car
except KeyboardInterrupt:
    stop()
