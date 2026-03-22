from gpiozero import LED
from time import sleep

# BCM 17번 핀에 연결된 LED 객체 생성
led = LED(17)

while True:
    led.on()   # LED 켜기
    sleep(1)   # 1초 대기
    led.off()  # LED 끄기
    sleep(1)   # 1초 대기
