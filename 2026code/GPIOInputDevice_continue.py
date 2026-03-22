from gpiozero import InputDevice
from time import sleep

sensor = InputDevice(21, pull_up=False)  # BOARD 40 → BCM 21

try:
    while True:
        readVal = int(sensor.is_active)
        print(readVal)
        sleep(1)
except KeyboardInterrupt:
    pass  # gpiozero는 자동 정리 — GPIO.cleanup() 불필요