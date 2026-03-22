from gpiozero import LED, Button
from time import sleep

led = LED(17)       # 17번 핀에 연결된 LED
button = Button(2)  # 2번 핀에 연결된 버튼

print("버튼을 누르세요...")
button.wait_for_press()  # 버튼이 눌릴 때까지 프로그램 대기

print("버튼이 눌렸습니다! LED를 켭니다.")
led.on()
sleep(3)                 # 3초간 켜진 상태 유지
led.off()