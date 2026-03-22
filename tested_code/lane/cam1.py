import time
import cv2
print(cv2.__version__)

dispW = 1280
dispH = 720

cam = cv2.VideoCapture('/dev/video0')
cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

while True:
    ret, frame = cam.read()
    cv2.imshow('Cam', frame)
    if cv2.waitKey(1) == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()