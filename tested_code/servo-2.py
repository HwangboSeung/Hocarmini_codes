import RPi.GPIO as GPIO 
from time import sleep  

servoPin          = 11   
SERVO_MAX_DUTY    = 12  
SERVO_MIN_DUTY    = 2    

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)        
GPIO.setup(servoPin, GPIO.OUT)  

servo = GPIO.PWM(servoPin, 50)  # 50Hz > 20ms
servo.start(0)  # duty = 0

def setServoPos(degree):
  if degree > 180:
    degree = 180

  duty = SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
  print("Degree: {} to {}(Duty)".format(degree, duty))

  servo.ChangeDutyCycle(duty)

if __name__ == "__main__":    
  setServoPos(50) # servo 0 degree
  sleep(1) # 1 sec waiting

  setServoPos(90)   # 90 degree
  sleep(1)

  setServoPos(130)  # 180 degree
  sleep(1)
  
  setServoPos(90)  # 90 degree
  sleep(1)
  
  servo.stop()  
  GPIO.cleanup()