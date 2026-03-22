import gpiod
import time

LED_PIN = 17

# 칩 객체 열기 (최신 커널은 'gpiochip0', 초기 버전은 'gpiochip4' 사용)
chip = gpiod.Chip('gpiochip0')

# 제어할 GPIO 라인(핀) 가져오기
line = chip.get_line(LED_PIN)

# 핀을 출력(Output) 방향으로 사용하겠다고 커널에 요청
line.request(consumer="LED_Blink", type=gpiod.LINE_REQ_DIR_OUT)

try:
    while True:
        line.set_value(1)  # LED 켜기 (HIGH)
        time.sleep(1)
        line.set_value(0)  # LED 끄기 (LOW)
        time.sleep(1)
finally:
    # 프로그램 종료 시 반드시 라인을 해제하여 자원을 반환
    line.release()