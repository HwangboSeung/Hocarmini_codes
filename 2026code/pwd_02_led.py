from gpiozero import PWMLED
from time import sleep

# GPIO 17번에 연결된 PWM 호환 LED 객체 생성
pwm_led = PWMLED(17)

print("밝기 0% (꺼짐)")
pwm_led.value = 0.0
sleep(2)

print("밝기 50% (중간 밝기)")
pwm_led.value = 0.5  # PWM 듀티비를 50%로 설정
sleep(2)

print("밝기 100% (최대 밝기)")
pwm_led.value = 1.0  # PWM 듀티비를 100%로 설정
sleep(2)

print("PWM 제어 종료")
pwm_led.off()