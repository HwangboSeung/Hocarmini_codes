from gpiozero import AngularServo
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device
from time import sleep

# 라즈베리 파이 5 호환성을 위해 핀 팩토리를 lgpio로 설정 [2]
Device.pin.factory = LGPIOFactory(chip=0)

# GPIO 18번 핀에 연결된 서보 모터 객체 생성
# (SG90 등 일반적인 서보모터 사양에 맞게 최소/최대 각도와 펄스 폭 설정)
servo = AngularServo(18, min_angle=-90, max_angle=90, min_pulse_width=0.0005, max_pulse_width=0.0024)

try:
    print("서보 모터 제어 시작 (종료하려면 Ctrl+C)")
    while True:
        print("최소 각도(-90도)로 이동")
        servo.angle = -90
        sleep(2)

        print("중앙(0도)으로 이동")
        servo.angle = 0
        sleep(2)

        print("최대 각도(+90도)로 이동")
        servo.angle = 90
        sleep(2)

except KeyboardInterrupt:
    print("프로그램을 종료합니다.")
    servo.detach() # 서보모터의 신호를 차단하여 안전하게 종료