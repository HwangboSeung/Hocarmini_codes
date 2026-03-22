from gpiozero import Motor
from time import sleep

# forward(IN1), backward(IN2), enable(ENA) 핀 지정
# enable 파라미터에 연결된 핀 번호를 넣으면 내부적으로 PWM 제어가 활성화됩니다.
motor = Motor(forward=4, backward=14, enable=18)

while True:
    print("최고 속도의 50%로 전진")
    # 0부터 1 사이의 값으로 속도(Duty Cycle) 지정
    motor.forward(speed=0.5)  
    sleep(2)
    
    print("최고 속도의 80%로 전진")
    motor.forward(speed=0.8)
    sleep(2)
    
    print("최고 속도의 30%로 후진")
    motor.backward(speed=0.3)
    sleep(2)
    
    print("정지")
    motor.stop()
    sleep(2)