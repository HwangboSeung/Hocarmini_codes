import cv2
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280,720)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

while True:
    im = picam2.capture_array()
    cv2.imshow('Image', im)
    if cv2.waitKey(1) == 27:  # ord('q')
      break

picam2.close()
cv2.destroyAllWindows()