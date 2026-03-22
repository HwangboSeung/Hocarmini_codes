#!/usr/bin/python3
import sys
import select
import time
from gpiozero import Button

from picamera2 import Picamera2, Preview

# Button is connected to GPIO 4
button = Button(4)

request = "none"

# Loop to keep taking photos
while True:
    picam2 = Picamera2()
    picam2.start_preview(Preview.QTGL)

    preview_config = picam2.create_preview_configuration()
    picam2.configure(preview_config)

    picam2.start()

    # Loop to wait on request
    while True:
        if button.is_pressed:
            request = "capture"
            break

        key_input = select.select([sys.stdin], [], [], 1)[0]
        if key_input:
            key_value = sys.stdin.readline().rstrip()
            # If q then quit
            if (key_value == "q"):
                request = "quit"
                break
            # Any other key capture
            else:
                request = "capture"
                break

    if request == "quit":
        break

    metadata = picam2.capture_file("captures/microscope-"+time.strftime("%Y%m%d-%H%M%S")+".jpg")
    print(metadata)
    picam2.close()

picam2.close()