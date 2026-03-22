import time
import cv2
from picamera2 import Picamera2

dispW = 1280; dispH = 720
fps = 0
pos = (30,60); font = cv2.FONT_HERSHEY_SIMPLEX
height = 1.5; myColor = (255,0,0); weight = 3

picam2 = Picamera2()
picam2.preview_configuration.main.size = (dispW,dispH)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.controls.FrameRate = 30
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

cam = cv2.VideoCapture('/dev/video0')
cam.set(cv2.CAP_PROP_FRAME_WIDTH, dispW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, dispH)

while True:
    tStart = time.time()
    #ret, im = cam.read()
    im = picam2.capture_array()
    #im = cv2.flip(im,=1)
    #im = cv2.cvtColr(im,cv2.COLOR_BGR2RGB)
    cv2.putText(im,str(int(fps))+' FPS', pos,font,height,myColor,weight)
    cv2.imshow('Cam', im)
    if cv2.waitKey(1) != -1:
        break
    tEnd = time.time()
    loopTime = tEnd - tStart
    fps = 0.9*fps + 0.1/loopTime
    print(fps)
    
picam2.close()
cv2.destroyAllWindows()
