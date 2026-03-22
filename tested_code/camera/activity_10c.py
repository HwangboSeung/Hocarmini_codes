import os
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

FOLDER_NAME = "/home/pi/activity_10"

if not os.path.exists(FOLDER_NAME):
    os.mkdir(FOLDER_NAME)
    
picam2 = Picamera2()
picam2.video_configuration.size = (640, 480)
encoder = H264Encoder(bitrate=10000000)

time.sleep(2)
picam2.start_recording(encoder, "test.h264", config="video")
counter = 1

try:
    while True:
        file_name = FOLDER_NAME + "/img" + str(counter) + ".jpg"
        counter += 1
        picam2.capture_file(file_name)
        print("New photo has been taken")
        time.sleep(5)
except KeyboardInterrupt:
    print("Ctrl + C is pressed.")

picam2.close()