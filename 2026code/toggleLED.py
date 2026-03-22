from gpiozero import LED, Button
from time import sleep

delay = 0.1
button = Button(21, pull_up=True)   # BOARD 40 → BCM 21
led    = LED(20)                     # BOARD 38 → BCM 20

LEDstate      = False
buttonStatOld = False  # 풀업: 미누름=False(HIGH=1), 누름=True(LOW=0)

try:
    while True:
        buttonState = button.is_pressed
        print(int(not buttonState))   # 원본과 동일한 출력값 유지 (미누름=1, 누름=0)

        # 버튼을 뗐을 때(False→False에서 누름→뗌) 토글
        # 원본: buttonState==1 and buttonStateOld==0
        # 풀업 변환: is_pressed==False and 이전==True (누름→뗌 엣지)
        if not buttonState and buttonStatOld:
            LEDstate = not LEDstate
            led.on() if LEDstate else led.off()

        buttonStatOld = buttonState
        sleep(delay)

except KeyboardInterrupt:
    led.off()
    led.close()
    button.close()
    print("Ctrl+C key is pressed")
