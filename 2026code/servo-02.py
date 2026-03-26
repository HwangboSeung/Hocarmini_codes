from gpiozero import Servo
from time import sleep
import os

# 라즈베리 파이 5에서 lgpio를 우선 사용하도록 설정 (환경 변수)
os.environ['GPIOZERO_PIN_FACTORY'] = 'lgpio'

# 서보 모터 설정 (BCM 18번 핀)
# Pi 5는 하드웨어 구조상 펄스 폭을 명시해주는 것이 더 정확합니다.
servo = Servo(18, min_pulse_width=0.9/1000, max_pulse_width=2.1/1000)

print("라즈베리 파이 5 모드에서 서보 작동 시작 (Ctrl+C로 종료)")

try:
    while True:
        servo.min()
        print("Min")
        sleep(2)
        
        servo.mid()
        print("Mid")
        sleep(2)
        
        servo.max()
        print("Max")
        sleep(2)

        servo.mid()
        print("Mid")
        sleep(2)

except KeyboardInterrupt:
    servo.value = None
    print("\n프로그램 종료")