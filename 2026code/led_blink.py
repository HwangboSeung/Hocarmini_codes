from gpiozero import LED
from signal import pause

led = LED(17)

try:
    led.blink(on_time=2, off_time=2)
    pause()
except KeyboardInterrupt:
    print("Ctrl+C가 눌러졌음")
    led.off()      # LED 명시적으로 끄기
    led.close()    # GPIO 핀 해제