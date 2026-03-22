from gpiozero import LED, Button
from signal import pause

led = LED(17)
button = Button(2)

# 버튼이 눌릴 때마다 LED 상태를 반전시킴
button.when_pressed = led.toggle

pause()