from gpiozero import LED
from time import sleep

# GPIO 17번에 연결된 LED 객체 생성
led = LED(17)

# LED 켜기
led.on()
print("LED가 켜졌습니다.")
sleep(2) # 2초 동안 대기

# LED 끄기
led.off()
print("LED가 꺼졌습니다.")