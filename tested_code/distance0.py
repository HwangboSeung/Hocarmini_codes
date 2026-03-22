import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) # GPIO.BCM

#set GPIO Pins
triger_pin = 2
echo_pin = 3

GPIO.setwarnings(False)

GPIO.setup(triger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

def distance() :    
    GPIO.output(triger_pin, True)
    time.sleep(0.00001)
    GPIO.output(triger_pin, False)
    
    StartTime = time.time()
    StopTime = time.time()
    
    # save time of arrival
    while (GPIO.input(echo_pin) == 0) :
        StartTime = time.time()
    
    # save time of arrival
    while (GPIO.input(echo_pin) == 1) :
        StopTime = time.time()
        
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    #multiply with the sonic speed (34300 cm/s) and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    
    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(0.2)
    
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
