from gpiozero import DistanceSensor
from signal import pause

# threshold_distance: 이벤트가 발생하는 임계 거리 설정 (기본값 0.3m) [4]
# max_distance: 센서가 측정할 최대 거리 설정 (기본값 1m) [5]
ultrasonic = DistanceSensor(echo=17, trigger=4, threshold_distance=0.5, max_distance=2.0)

def in_range_action():
    print("경고: 장애물이 50cm 이내로 접근했습니다!")

def out_of_range_action():
    print("안전: 장애물이 멀어졌습니다.")

# 거리가 0.5m 이내가 되면 in_range_action 함수 실행 [3]
ultrasonic.when_in_range = in_range_action

# 거리가 0.5m 밖으로 벗어나면 out_of_range_action 함수 실행 [3]
ultrasonic.when_out_of_range = out_of_range_action

print("거리 감지를 시작합니다. (종료하려면 Ctrl+C)")
pause()