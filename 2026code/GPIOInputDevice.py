from gpiozero import InputDevice

sensor = InputDevice(21, pull_up=False)
realVal = int(sensor.is_active)
print(realVal)