from gpiozero import LED, Button
from signal import pause

led = LED(17)
button = Button(2)

# 버튼이 눌리면 led.on 함수를 실행하고, 떼어지면 led.off 함수를 실행
button.when_pressed = led.on
button.when_released = led.off

print("버튼을 눌렀다 떼어보세요. (종료하려면 Ctrl+C)")

# 프로그램이 즉시 종료되지 않고 계속 백그라운드에서 이벤트를 감지하도록 대기
pause() 