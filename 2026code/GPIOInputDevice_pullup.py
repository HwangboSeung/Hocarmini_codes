from gpiozero import InputDevice

sensor = InputDevice(21, pull_up=True)
realVal = int(not sensor.is_active)  # ← not 추가
print(realVal)