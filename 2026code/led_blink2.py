from gpiozero import LED
from time import sleep

led = LED(17)

try:
    while True:
        led.on()
        sleep(2)
        led.off()
        sleep(2)
except KeyboardInterrupt:
    print("Ctrl+C가 눌러졌음")
    led.off()