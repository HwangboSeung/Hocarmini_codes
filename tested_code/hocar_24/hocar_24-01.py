import os, struct, array, select
from fcntl import ioctl
from hocar import Hocar  
import RPi.GPIO as GPIO
from time import sleep

# parameters
init_speed = 0
center_angle = 90
dist_limit = 25.0  # cm

# Hocar class : ENA, IN1, IN2, ENS, speed, angle, dist_limit
car = Hocar(init_speed, center_angle, dist_limit) 

state = 1  # FORWARD =1, BACKWARD=2, STOP=0
speed = 0
angle = center_angle

# Iterate over the joystick devices.
print('Available devices:')

for fn in os.listdir('/dev/input'):
    if fn.startswith('js'):
        print('  /dev/input/%s' % (fn))

# We'll store the states here.
axis_states = {}
button_states = {}

# These constants were borrowed from linux/input.h
axis_names = {
    0x00 : 'x',
    0x01 : 'y',
    0x02 : 'z',
    0x03 : 'rx',
    0x04 : 'ry',
    0x05 : 'rz',
    0x06 : 'trottle',
    0x07 : 'rudder',
    0x08 : 'wheel',
    0x09 : 'gas',
    0x0a : 'brake',
    0x10 : 'hat0x',
    0x11 : 'hat0y',
    0x12 : 'hat1x',
    0x13 : 'hat1y',
    0x14 : 'hat2x',
    0x15 : 'hat2y',
    0x16 : 'hat3x',
    0x17 : 'hat3y',
    0x18 : 'pressure',
    0x19 : 'distance',
    0x1a : 'tilt_x',
    0x1b : 'tilt_y',
    0x1c : 'tool_width',
    0x20 : 'volume',
    0x28 : 'misc',
}

button_names = {
    0x120 : 'trigger',
    0x121 : 'thumb',
    0x122 : 'thumb2',
    0x123 : 'top',
    0x124 : 'top2',
    0x125 : 'pinkie',
    0x126 : 'base',
    0x127 : 'base2',
    0x128 : 'base3',
    0x129 : 'base4',
    0x12a : 'base5',
    0x12b : 'base6',
    0x12f : 'dead',
    0x130 : 'a',
    0x131 : 'b',
    0x132 : 'c',
    0x133 : 'x',
    0x134 : 'y',
    0x135 : 'z',
    0x136 : 'tl',
    0x137 : 'tr',
    0x138 : 'tl2',
    0x139 : 'tr2',
    0x13a : 'select',
    0x13b : 'start',
    0x13c : 'mode',
    0x13d : 'thumbl',
    0x13e : 'thumbr',

    0x220 : 'dpad_up',
    0x221 : 'dpad_down',
    0x222 : 'dpad_left',
    0x223 : 'dpad_right',

    # XBox 360 controller 
    0x2c0 : 'dpad_left',
    0x2c1 : 'dpad_right',
    0x2c2 : 'dpad_up',
    0x2c3 : 'dpad_down',
}

axis_map = []
button_map = []

# Open the joystick device.
fn = '/dev/input/js0'
print('Opening %s...' % fn)
jsdev = open(fn, 'rb' )

# Get the device name.
#buf = bytearray(63)
buf = array.array('B', [0] * 64)
ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
js_name = buf.tobytes().rstrip(b'\x00').decode('utf-8')
print('Device name: %s' % js_name)

# Get the number of axes and buttons.
buf = array.array('B', [0])
ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
num_axes = buf[0]

buf = array.array('B', [0])
ioctl(jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
num_buttons = buf[0]

# Get the axis map.
buf = array.array('B', [0] * 0x40)
ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP

for axis in buf[:num_axes]:
    axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
    axis_map.append(axis_name)
    axis_states[axis_name] = 0.0

# Get the button map.
buf = array.array('H', [0] * 200)
ioctl(jsdev, 0x80406a34, buf) # JSIOCGBTNMAP

for btn in buf[:num_buttons]:
    btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
    button_map.append(btn_name)
    button_states[btn_name] = 0

print('%d axes found: %s' % (num_axes, ', '.join(axis_map))) # 6 axes found: x, y, z, rz, hat0x, hat0y
print('%d buttons found: %s' % (num_buttons, ', '.join(button_map))) # 12 buttons found: a, b, c, x, y, z, tl, tr, tl2, tr2, select, start


# Main event loop
while True:
    car.setMotorControl(car.speed, state)
    sleep(0.1)
    dist = car.measureDistance()
    # print("Measured Distance = %.1f cm" % dist)

    # rrdy, _, _ = select.select([jsdev], [], [], 1) 
    # evbuf = os.read(jsdev.fileno(), 8) if (rrdy!=[]) else ""
    evbuf = os.read(jsdev.fileno(), 8)
    
    if evbuf:
        time, value, type, number = struct.unpack('IhBB', evbuf)

        if type & 0x80:
             print("(initial)", end="")
             
        # button pressesed or released
        if type & 0x01:  
            button = button_map[number]
            if button:
                button_states[button] = value
                if value:
                    print("%s pressed" % (button))
                    # if button is LB at left front, then stop 
                    if button == 'y':
                        state = car.STOP
                        car.setMotorControl(0, state)
                        GPIO.cleanup()
                        print('stop')
                        break
                    elif button == 'z':
                        state = car.FORWARD
                        print('direction is forward')
                        car.setMotorControl(0, state) # stop and reverse
                        sleep(0.5)
                        car.setMotorControl(normal_speed, state)
                    elif button == 'tr':
                        state = car.BACKWARD
                        print('direction is backward')
                        car.setMotorControl(0, state) # stop and reverse
                        sleep(0.5)
                        car.setMotorControl(normal_speed, state)
                    elif button == 'tl':
                        car.setServoAngle(90)
                        # car.setMotorControl(0, state)
                    # sleep(0.2)

                car.setMotorControl(car.speed, state)
                # speed = car.speed  # obstacle detected
                
        # axis & fvalue
        if type & 0x02:
            axis = axis_map[number]
            if axis:
                fvalue = value / 32767.0  # value / 32767.0
                axis_states[axis] = fvalue                
                print("%s: %.3f" % (axis, fvalue))
                
                x = axis_states['x'] # get x-axis state value 
                y = axis_states['y'] # get y-axis state value 

                if y != 0:    # if y-axis is not in the center
                    if y > 0:    # if y > 0
                        speed -= 10
                        if speed < 0 : speed = 0                    
                    else:      # if y < 0
                        speed += 10
                        if speed > car.max_speed : 
                            speed = car.max_speed
                    car.setMotorControl(speed, car.state) # ; speed = car.speed
                    print('Current speed : ', speed)

                elif x != 0:                    
                    if x > 0:   # if x > 0
                        angle += 10
                        if angle > car.max_steering : 
                            angle = car.max_steering
                    else:   # if x < 0
                        angle -= 10
                        if angle < car.min_steering : 
                            angle = car.min_steering
                    car.setServoAngle(angle)
                    print('Current angle : ', angle)
                else:   
                    # if x, y in 0 position
                    car.setMotorControl(car.speed, car.state)
                    car.setServoAngle(car.angle)
     