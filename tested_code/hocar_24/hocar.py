#!/usr/bin/python3
import RPi.GPIO as GPIO          
import time

# Hocar class
class Hocar:
    def __init__(self, speed=50, angle=90, object_distance=30):
        # Pin setup
        self.enAPin = 25  # 16, DC Motor ENA pin
        self.inPin1 = 24  # 20, DC Motor
        self.inPin2 = 23  # 21, DC Motor
        self.enSPin = 17  # 12, Servo Motor
        self.triger_pin = 27  # 18, Ultrasonic sensor
        self.echo_pin = 22  # 24, Ultrasonic sensor

        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)  # Disable warnings

        GPIO.setup(self.enAPin, GPIO.OUT)
        GPIO.setup(self.inPin1, GPIO.OUT)
        GPIO.setup(self.inPin2, GPIO.OUT)
        GPIO.setup(self.enSPin, GPIO.OUT)
        GPIO.setup(self.triger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

        # PWM setup
        self.dc_pwm = GPIO.PWM(self.enAPin, 1000)  # DC Motor
        self.dc_pwm.start(0)
        self.servo_pwm = GPIO.PWM(self.enSPin, 50)  # Servo Motor
        self.servo_pwm.start(0)

        # Initial values
        self.speed = speed  # 0 ~ 100
        self.max_speed = 80
        self.angle = angle  # 40 ~ 140
        self.distance = None
        self.prev_distance = 50  # cm
        self.max_distance = 400  # cm
        self.prev_ratio = 0.5
        self.detection_limit = object_distance  # cm
        self.max_steering = 120
        self.min_steering = 60

        # Motor states
        self.state = 1  # STOP = 0, FORWARD = 1, BACKWARD = 2

    def setMotorControl(self, speed=50, state=1):
        distance = self.measureDistance()
        self.state = state

        if (distance < self.detection_limit) and (self.state == 1):
            self.speed = 0
            self.state = 0 # STOP 
            print('Obstacle detected')
        else:
            self.speed = speed
            print("Measured Distance = %.1f cm" % distance)

        # Motor control PWM
        self.dc_pwm.ChangeDutyCycle(self.speed)

        if self.state == 1:   # FORWARD
            GPIO.output(self.inPin1, True)
            GPIO.output(self.inPin2, False)
            print('forward...')
        elif self.state == 2:   # BACKWARD
            GPIO.output(self.inPin1, False)
            GPIO.output(self.inPin2, True)
            print('backward...')
        else:  # STOP
            GPIO.output(self.inPin1, False)
            GPIO.output(self.inPin2, False)
            print('stop')

    def setServoAngle(self, angle):
        if angle > self.max_steering:  # max steering angle
            angle = self.max_steering
        if angle < self.min_steering:  # min steering angle
            angle = self.min_steering
        self.angle = angle
        duty = self.angle / 18 + 2.5
        GPIO.output(self.enSPin, True)
        self.servo_pwm.ChangeDutyCycle(duty)
        time.sleep(0.1)

    def measureDistance(self):
        echo_start = 0
        echo_stop = 0

        GPIO.output(self.triger_pin, True)
        time.sleep(0.00001)  # default 0.00001
        GPIO.output(self.triger_pin, False)

        # Save time of arrival
        while GPIO.input(self.echo_pin) == 0:
            echo_start = time.time()

        # Save time of arrival
        while GPIO.input(self.echo_pin) == 1:
            echo_stop = time.time()

        # Time difference between start and arrival
        elapsed_time = echo_stop - echo_start

        # Multiply with the sonic speed (34300 cm/s) and divide by 2, because there and back
        self.distance = (elapsed_time * 34300) / 2

        if self.distance > self.max_distance:
            self.distance = self.max_distance

        # Complementary filter
        self.distance = self.prev_distance * self.prev_ratio + self.distance * (1 - self.prev_ratio)
        self.prev_distance = self.distance
        time.sleep(0.1)
        return self.distance

    def __del__(self):
        # Cleanup
        self.speed = 0
        self.angle = 90
        self.dc_pwm.stop()
        self.servo_pwm.stop()
        GPIO.cleanup()
        time.sleep(1)

# Test the Hocar class
if __name__ == "__main__":
    car = Hocar()

    for i in range(3):
        car.setMotorControl(50, 1)
        car.setServoAngle(120)
        time.sleep(1)

    for i in range(2):
        car.setMotorControl(0, 0)
        car.setServoAngle(90)
        time.sleep(1)

    for i in range(3):
        car.setMotorControl(50, 2)
        car.setServoAngle(70)
        time.sleep(1)

    car.setMotorControl(0, 0)
    car.setServoAngle(90)
    time.sleep(1)

    for i in range(5):
        dist = car.measureDistance()
        print("Measured Distance = %.1f cm" % dist)
        time.sleep(0.2)

    GPIO.cleanup()
