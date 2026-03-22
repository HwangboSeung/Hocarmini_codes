import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD) # GPIO.BCM
servo_pin = 11

GPIO.setwarnings(False)
GPIO.setup(servo_pin, GPIO.OUT)

pwm=GPIO.PWM(servo_pin, 50) # 50Hz PWM
pwm.start(0)

pwm.ChangeDutyCycle(5) # 5-> left -90 deg position
sleep(2)
pwm.ChangeDutyCycle(7.5) # neutral position
sleep(2)
pwm.ChangeDutyCycle(10) # 10->right +90 deg position
sleep(2)
pwm.ChangeDutyCycle(7.5) # neutral position
sleep(1)

pwm.stop() 
GPIO.cleanup()
