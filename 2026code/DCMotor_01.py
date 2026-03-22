from gpiozero import Motor
from time import sleep

# 전진(forward) 핀을 GPIO 4로, 후진(backward) 핀을 GPIO 14로 설정
motor = Motor(forward=4, backward=14)

while True:
    print("앞으로 회전")
    motor.forward(0.5)  # 모터 전진 작동
    sleep(2)
    
    print("뒤로 회전")
    motor.backward() # 모터 역방향(후진) 작동
    sleep(2)
    
    print("정지")
    motor.stop()     # 모터 정지
    sleep(2)