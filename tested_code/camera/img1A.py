import cv2
from picamera2 import Picamera2
import time

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640,480)}))
picam2.start()

cpt = 0
maxFrames = 30
while cpt < maxFrames:
    im= picam2.capture_array()
    #im=cv2.flip(im,-1)
    cv2.imshow("Camera", im)
    cv2.imwrite('/home/pi/dataset/images/arduino_uno_%d.jpg' %cpt, im)
    cpt += 1
    if cv2.waitKey(1)==ord('q'):
        break
cv2.destroyAllWindows()