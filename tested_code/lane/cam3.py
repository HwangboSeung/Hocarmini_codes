import cv2
from picamera2 import Picamera2

dispW = 1280; dispH = 720

picam2 = Picamera2()
picam2.preview_configuration.main.size = (dispW,dispH)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 30
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

while True:
    im = picam2.capture_array()
    cv2.imshow('camera', im)
    
    if cv2.waitKey(1) != -1:
        cv2.imwrite('photo.jpg', im)
        picam2.capture_file('photo2.jpg')
        break

picam2.close()
cv2.destroyAllWindows()
