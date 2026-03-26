from gpiozero import Servo
from time import sleep

# BCM 18번 핀에 서보 모터 연결
servo = Servo(18)

while True:
    servo.min()  # 서보 모터를 최소 위치(보통 -90도)로 이동
    sleep(2)
    
    servo.mid()  # 서보 모터를 중간 위치(0도)로 이동
    sleep(2)
    
    servo.max()  # 서보 모터를 최대 위치(보통 +90도)로 이동
    sleep(2)

    servo.mid()  # 서보 모터를 중간 위치(0도)로 이동
    sleep(2)
    