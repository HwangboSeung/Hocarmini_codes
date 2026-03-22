import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD) # GPIO.BCM
servo_pin =11 

GPIO.setwarnings(False)
GPIO.setup(servo_pin, GPIO.OUT)

pwm=GPIO.PWM(servo_pin, 50) # 50Hz PWM
pwm.start(0)

def setAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    #GPIO.output(servo_pin, False)
    #pwm.ChangeDutyCycle(duty)

setAngle(50) # 5-> left -90 deg position
setAngle(90) # neutral position
setAngle(130) # 10->right +90 deg position
setAngle(90) # neutral position

pwm.stop() 
GPIO.cleanup()