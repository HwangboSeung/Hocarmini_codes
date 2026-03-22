from gpiozero import LED
from signal import pause

led = LED(17)

# 1초 동안 켜지고 1초 동안 꺼지는 것을 무한히 반복
led.blink(on_time=1, off_time=1)

# 코드가 종료되지 않고 계속 백그라운드에서 깜빡이도록 유지
pause() 