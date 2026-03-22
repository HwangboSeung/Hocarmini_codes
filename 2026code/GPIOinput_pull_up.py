from gpiozero import Button

# BOARD 핀 40 → BCM 핀 21
button = Button(21)

realVal = 1 if not button.is_pressed else 0
print(realVal)