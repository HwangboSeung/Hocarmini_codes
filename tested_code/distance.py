import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 27
ECHO = 22
print("Ultrasonic measurement")

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print("Initialization")
time.sleep(2)

try:
    while True:
        GPIO.output(TRIG,True)
        time.sleep(0.00001)        
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO)==0:
            start = time.time()     
            
        while GPIO.input(ECHO)==1:
            stop = time.time()      

        check_time = stop - start
        distance = check_time * 34300 / 2
        print("Distance : %.1f cm" % distance)
        time.sleep(0.4)
        
except KeyboardInterrupt:
    print("Finished")
    GPIO.cleanup()      
        

