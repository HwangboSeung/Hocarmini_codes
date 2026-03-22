import time
import cv2
from picamera2 import Picamera2

dispW, dispH = 1280, 720
pos = (30, 60)
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1.5
color = (255, 0, 0)
thickness = 3

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (dispW, dispH)},
                                             controls={"FrameRate": 30})
picam2.configure(config)
picam2.start()

fps = 0

while True:
    tStart = time.time()

    frame = picam2.capture_array()
    
    cv2.putText(frame, f'{int(fps)} FPS', pos, font, fontScale, color, thickness)
    cv2.imshow('PiCamera', frame)

    if cv2.waitKey(1) != -1:
        break

    loopTime = time.time() - tStart
    fps = (fps * 0.9) + (0.1 / loopTime)
    print(fps)

picam2.stop()
cv2.destroyAllWindows()

