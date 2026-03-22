import os, struct, array
from fcntl import ioctl
from hocar import Hocar  
import RPi.GPIO as GPIO
from time import sleep

# check joystick
print('Available devices:')
for fn in os.listdir('/dev/input'):
    if fn.startswith('js'):
        print('    /dev/input/%s' % (fn))

# store axis & button values
axis_states = {}
button_states = {}

# Map joystick constants from linux/input.h
axis_names = {
    0x00: 'x', 0x01: 'y', 0x02: 'z', 0x03: 'rx', 0x04: 'ry', 0x05: 'rz',
    0x06: 'trottle', 0x07: 'rudder', 0x08: 'wheel', 0x09: 'gas', 0x0a: 'brake',
    0x10: 'hat0x', 0x11: 'hat0y', 0x12: 'hat1x', 0x13: 'hat1y', 0x14: 'hat2x',
    0x15: 'hat2y', 0x16: 'hat3x', 0x17: 'hat3y', 0x18: 'pressure', 0x19: 'distance',
    0x1a: 'tilt_x', 0x1b: 'tilt_y', 0x1c: 'tool_width', 0x20: 'volume', 0x28: 'misc',
}

button_names = {
    0x120: 'trigger', 0x121: 'thumb', 0x122: 'thumb2', 0x123: 'top', 0x124: 'top2',
    0x125: 'pinkie', 0x126: 'base', 0x127: 'base2', 0x128: 'base3', 0x129: 'base4',
    0x12a: 'base5', 0x12b: 'base6', 0x12f: 'dead', 0x130: 'a', 0x131: 'b', 0x132: 'c',
    0x133: 'x', 0x134: 'y', 0x135: 'z', 0x136: 'tl', 0x137: 'tr', 0x138: 'tl2', 0x139: 'tr2',
    0x13a: 'select', 0x13b: 'start', 0x13c: 'mode', 0x13d: 'thumbl', 0x13e: 'thumbr',
    0x220: 'dpad_up', 0x221: 'dpad_down', 0x222: 'dpad_left', 0x223: 'dpad_right',
    0x2c0: 'dpad_left', 0x2c1: 'dpad_right', 0x2c2: 'dpad_up', 0x2c3: 'dpad_down',
}

axis_map = []
button_map = []

# Open the joystick device (/de/inpuyt/js0)
fn = '/dev/input/js0'
print('Opening %s...' % fn)
jsdev = open(fn, 'rb')

# Get the device name
buf = array.array('B', [0] * 64)
ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
js_name = buf.tobytes().rstrip(b'\x00').decode('utf-8')
print('Device name: %s' % js_name)

# Get number of axes and buttons from driver.
buf = array.array('B', [0])
ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
num_axes = buf[0]  # axes --> 6

buf = array.array('B', [0])
ioctl(jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
num_buttons = buf[0]  # buttons --> 12

# Get the axis map from axis_names.
buf = array.array('B', [0] * 0x40)
ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP

for axis in buf[:num_axes]:
    axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis) # x, y, z, rz, hat0x, hat0y
    axis_map.append(axis_name)
    axis_states[axis_name] = 0.0

# Get the button map from button_name.
buf = array.array('H', [0] * 200)
ioctl(jsdev, 0x80406a34, buf) # JSIOCGBTNMAP

for btn in buf[:num_buttons]:
    btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn) # a, b, c, x, y, z, tl, tr, tl2, tr2, select, start
    button_map.append(btn_name)
    button_states[btn_name] = 0

print('%d axes found: %s' % (num_axes, ', '.join(axis_map)))
print('%d buttons found: %s' % (num_buttons, ', '.join(button_map)))

# Parameters
init_speed = 0
center_angle = 90
object_distance = 25.0  # cm

# Hocar class initialization
car = Hocar(init_speed, center_angle, object_distance) 

state = 1  # FORWARD = 1, BACKWARD = 2, STOP = 0
speed = 50
angle = center_angle


# Main event loop
try:
    while True:
        evbuf = os.read(jsdev.fileno(), 8)
        
        dist = car.measureDistance()
        # print(f"Measured Distance = {dist:.1f} cm")

        if evbuf:    # if event happened
            time, value, type, number = struct.unpack('IhBB', evbuf)

            # if type==0x01, pressed or released
            if type & 0x01:
                button = button_map[number]
                if button:             
                    button_states[button] = value
                    if value:
                        print("%s pressed" % (button))
                        if button == 'y':  # Stop the car
                            state = 0 # STOP
                            car.setMotorControl(0, state)
                            GPIO.cleanup()
                            print('stop')
                            break
                        elif button == 'z':  # Move forward
                            print('direction is forward')
                            if state == 2:
                                car.setMotorControl(0, 0)
                                sleep(1)
                            state = 1  # FORWARD
                            car.setMotorControl(speed, state)
                        elif button == 'tr':  # Move backward                            
                            print('direction is backward')
                            if state == 1:
                                car.setMotorControl(0, 0)
                                sleep(1)
                            state = 2 # BACKWARD
                            car.setMotorControl(speed, state)
                        elif button == 'tl':  # Center the servo
                            car.setServoAngle(center_angle)
                        else :
                            pass
                        sleep(0.1)

            # if type==0x02, axis move
            if type & 0x02:
                axis = axis_map[number]
                if axis:
                    # -32767 ~ 0 ~ 32767 
                    fvalue = value / 32767.0
                    # save state value (0, 1, -1)
                    axis_states[axis] = fvalue
                    print("%s: %.3f" % (axis, fvalue))
                    
                    x = axis_states['x']
                    y = axis_states['y']
                    
                    if y != 0:  # Adjust speed based on y-axis
                        if y > 0:
                            speed = max(0, speed - 5)
                        else:
                            speed = min(car.max_speed, speed + 5)
                        car.setMotorControl(speed, car.state)
                        print(f'Speed: {speed}')

                    elif x != 0:  # Adjust angle based on x-axis
                        if x > 0:
                            angle = min(car.max_steering, angle + 10)
                        else:
                            angle = max(car.min_steering, angle - 10)
                        car.setServoAngle(angle)
                        print(f'Angle: {angle}')
                    else:
                        car.setMotorControl(car.speed, car.state)
                        car.setServoAngle(car.angle)
                    #sleep(0.05)
                
except KeyboardInterrupt:
    print('Ctrl+C is pressed')
    car.setMotorControl(0, 0)
    car.setServoAngle(90)
    car.dc_pwm.stop()
    car.servo_pwm.stop()
    GPIO.cleanup()
    sleep(1)