from gpiozero import DistanceSensor
from time import sleep

# DistanceSensor 객체 생성 (사용할 GPIO 핀 번호 지정)
# 주의: echo 핀 연결 시 반드시 전압 분배 회로를 거쳐야 합니다!
sensor = DistanceSensor(echo=24, trigger=23)

while True:
    # sensor.distance는 측정된 거리를 '미터(m)' 단위로 자동 반환합니다.
    distance_cm = sensor.distance * 100
    
    print(f"측정된 거리: {distance_cm:.1f} cm")
    
    # 1초마다 반복 측정
    sleep(1)