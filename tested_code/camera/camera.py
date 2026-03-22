from picamera2 import Picamera2, Preview
from libcamera import Transform
import time

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL, x=100, y=200, width=800, height=600,
                    transform=Transform(vflip=1)) # x, y:  the starting position on the screen
picam2.start()
time.sleep(2)

file_name = "/home/pi/camera/image.jpg"
picam2.capture_file(file_name)
print("Done")

picam2.stop_preview()
picam2.close()