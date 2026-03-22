#!/usr/bin/python
import RPi.GPIO as GPIO          
from time import sleep, time

in1 = 24
in2 = 23
ena = 25
servo = 17

straight_time = 5
curve_time = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(ena, GPIO.OUT)
GPIO.setup(servo, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)

servo_pwm = GPIO.PWM(servo, 50)
dc_pwm=GPIO.PWM(ena,1000)
servo_pwm.start(0)
dc_pwm.start(15)

def setAngle(angle):
    duty = angle / 36 + 5
    GPIO.output(servo, True)
    servo_pwm.ChangeDutyCycle(duty)
    sleep(0.1)

print("\n")
print("Start the Mission 8.....")
print("\n")

dc_pwm.ChangeDutyCycle(40)
GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.LOW)
sleep(1)  # for start delay
start_time = time()  

try:
    while(1):
        #sleep(0.01)
        current_time = time()
        elapse_time = current_time - start_time 
        if elapse_time < straight_time :
            print("1-Straight region")
            setAngle(90)
            dc_pwm.ChangeDutyCycle(30)
        elif elapse_time < straight_time + curve_time :
            print("1-Curve region")
            setAngle(140)
            dc_pwm.ChangeDutyCycle(35)
        elif elapse_time < straight_time * 2 + curve_time :
            print("2-Straight region")
            setAngle(90)
            dc_pwm.ChangeDutyCycle(20)
        elif elapse_time < (straight_time + curve_time) * 2 :    
            print("2-Curve region")
            setAngle(40)
            dc_pwm.ChangeDutyCycle(30)
        else :
            print("2-Curve region")
            setAngle(90)
            dc_pwm.ChangeDutyCycle(0)
            sleep(1)
            current_time = start_time
            break
except KeyboardInterrupt:
    print("Ctrl+C is pressed")
    
GPIO.cleanup()
print("Stop with clean up")