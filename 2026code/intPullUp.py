from gpiozero import LED, Button
from time import sleep

delay = 0.1
button = Button(21, pull_up=True)   # BOARD 40 → BCM 21, 풀업
led    = LED(20)                    # BOARD 38 → BCM 20

try:
    while True:
        realVal = int(not button.is_pressed)
        print(realVal)
        if button.is_pressed:       # realVal == 0 → LED 켜기
            led.on()
        else:                       # realVal == 1 → LED 끄기
            led.off()
        sleep(delay)
except KeyboardInterrupt:
    led.off()
    led.close()
    button.close()
    print("Ctrl+C key is pressed")