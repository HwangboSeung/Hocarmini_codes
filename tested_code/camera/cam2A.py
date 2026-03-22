import cv2
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640,480)}))
picam2.start()

while True:
    frame = picam2.capture_array()

    cv2.imshow("Pi Camera", frame)

    if cv2.waitKey(1) != -1:
        break

cv2.destroyAllWindows()
picam2.stop()
