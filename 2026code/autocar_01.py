from gpiozero import Robot, DistanceSensor
from time import sleep
from signal import pause
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device

# 라즈베리 파이 5 호환성을 위한 설정 (필요시)
Device.pin.factory = LGPIOFactory(chip=0)

# 1. 왼쪽 바퀴와 오른쪽 바퀴가 연결된 핀 번호 설정
# 괄호 안의 숫자는 (전진 핀, 후진 핀)을 의미합니다.
robot = Robot(left=(4, 14), right=(17, 27)) # [2]

# 2. 초음파 센서 설정
# threshold_distance: 장애물로 인식할 거리 (단위: 미터, 0.3 = 30cm)
sensor = DistanceSensor(echo=23, trigger=22, threshold_distance=0.3) # [1, 7]

# 3. 장애물을 감지했을 때 실행할 회피 행동 함수 정의
def avoid_obstacle():
    print("장애물 감지! 회피 기동을 시작합니다.")
    robot.stop()           # 먼저 멈춤 [8]
    sleep(0.5)
    
    print("뒤로 이동...")
    robot.backward(0.5)    # 50% 속도로 후진 [8]
    sleep(1)               # 1초간 유지
    
    print("우회전...")
    robot.right(0.5)       # 50% 속도로 제자리 우회전 (왼쪽 바퀴 전진, 오른쪽 바퀴 후진) [8]
    sleep(0.5)             # 0.5초간 유지 (각도 조절)
    
    print("회피 완료, 다시 전진합니다.")
    robot.forward(0.5)     # 다시 앞으로 이동 [2]

# 4. 센서 범위 내(30cm 이내)에 물체가 들어오면 avoid_obstacle 함수 자동 실행
sensor.when_in_range = avoid_obstacle # [6]

# 5. 메인 프로그램 시작
print("자율주행을 시작합니다. (종료하려면 Ctrl+C)")
robot.forward(0.5)         # 50% 속도로 기본 직진 시작 [2]

# 프로그램이 종료되지 않도록 백그라운드 대기
pause()