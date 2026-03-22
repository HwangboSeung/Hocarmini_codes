import time
import cv2
from picamera2 import Picamera2

START_TIME = time.time()
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640,480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Continuously capture images from the camera 
while True:
    im = picam2.capture_array()  
    image=cv2.resize(im,(640,480))
    # image = cv2.flip(image, -1)

    # rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imshow('Image', image)

    # Stop the program if the ESC key is pressed.
    if cv2.waitKey(1) == 27:
      break

picam2.close()
cv2.destroyAllWindows()