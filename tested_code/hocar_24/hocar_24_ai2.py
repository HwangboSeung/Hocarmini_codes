import os
import struct
import array
from fcntl import ioctl
from hocar import Hocar  
import RPi.GPIO as GPIO
from time import sleep
import logging

# Constants and Configuration
INIT_SPEED = 0
CENTER_ANGLE = 90
OBJECT_DISTANCE = 25.0  # cm
JOYSTICK_DEVICE = '/dev/input/js0'
AXIS_NAMES = {
    0x00: 'x', 0x01: 'y', 0x02: 'z', 0x03: 'rx', 0x04: 'ry', 0x05: 'rz',
    0x06: 'trottle', 0x07: 'rudder', 0x08: 'wheel', 0x09: 'gas', 0x0a: 'brake',
    0x10: 'hat0x', 0x11: 'hat0y', 0x12: 'hat1x', 0x13: 'hat1y', 0x14: 'hat2x',
    0x15: 'hat2y', 0x16: 'hat3x', 0x17: 'hat3y', 0x18: 'pressure', 0x19: 'distance',
    0x1a: 'tilt_x', 0x1b: 'tilt_y', 0x1c: 'tool_width', 0x20: 'volume', 0x28: 'misc',
}
BUTTON_NAMES = {
    0x120: 'trigger', 0x121: 'thumb', 0x122: 'thumb2', 0x123: 'top', 0x124: 'top2',
    0x125: 'pinkie', 0x126: 'base', 0x127: 'base2', 0x128: 'base3', 0x129: 'base4',
    0x12a: 'base5', 0x12b: 'base6', 0x12f: 'dead', 0x130: 'a', 0x131: 'b', 0x132: 'c',
    0x133: 'x', 0x134: 'y', 0x135: 'z', 0x136: 'tl', 0x137: 'tr', 0x138: 'tl2', 0x139: 'tr2',
    0x13a: 'select', 0x13b: 'start', 0x13c: 'mode', 0x13d: 'thumbl', 0x13e: 'thumbr',
    0x220: 'dpad_up', 0x221: 'dpad_down', 0x222: 'dpad_left', 0x223: 'dpad_right',
    0x2c0: 'dpad_left', 0x2c1: 'dpad_right', 0x2c2: 'dpad_up', 0x2c3: 'dpad_down',
}

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Joystick States
axis_states = {}
button_states = {}

# Axis and Button Maps
axis_map = []
button_map = []

def check_joystick():
    """Check and list available joystick devices."""
    logger.info('Available devices:')
    for fn in os.listdir('/dev/input'):
        if fn.startswith('js'):
            logger.info(f'/dev/input/{fn}')

def open_joystick():
    """Open the joystick device and get its name."""
    try:
        jsdev = open(JOYSTICK_DEVICE, 'rb')
    except FileNotFoundError:
        logger.error(f"Joystick device {JOYSTICK_DEVICE} not found.")
        exit(1)

    # Get the device name
    buf = array.array('B', [0] * 64)
    ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf)  # JSIOCGNAME(len)
    js_name = buf.tobytes().rstrip(b'\x00').decode('utf-8')
    logger.info(f'Device name: {js_name}')
    return jsdev

def get_joystick_info(jsdev):
    """Get joystick axis and button mappings."""
    # Get number of axes and buttons from driver
    buf = array.array('B', [0])
    ioctl(jsdev, 0x80016a11, buf)  # JSIOCGAXES
    num_axes = buf[0]

    buf = array.array('B', [0])
    ioctl(jsdev, 0x80016a12, buf)  # JSIOCGBUTTONS
    num_buttons = buf[0]

    # Get the axis map from AXIS_NAMES
    buf = array.array('B', [0] * 0x40)
    ioctl(jsdev, 0x80406a32, buf)  # JSIOCGAXMAP
    for axis in buf[:num_axes]:
        axis_name = AXIS_NAMES.get(axis, f'unknown(0x{axis:02x})')
        axis_map.append(axis_name)
        axis_states[axis_name] = 0.0

    # Get the button map from BUTTON_NAMES
    buf = array.array('H', [0] * 200)
    ioctl(jsdev, 0x80406a34, buf)  # JSIOCGBTNMAP
    for btn in buf[:num_buttons]:
        btn_name = BUTTON_NAMES.get(btn, f'unknown(0x{btn:03x})')
        button_map.append(btn_name)
        button_states[btn_name] = 0

    logger.info(f'{num_axes} axes found: {", ".join(axis_map)}')
    logger.info(f'{num_buttons} buttons found: {", ".join(button_map)}')

def handle_button_event(button, value, car, state, speed, angle):
    """Handle joystick button events."""
    if button and value:
        logger.info(f"{button} pressed")
        if button == 'y':  # Stop the car
            state = 0  # STOP
            car.setMotorControl(0, state)
            #GPIO.cleanup()
            logger.info('Stop')
            exit(0)
        elif button == 'z':  # Move forward
            if state == 2:
                car.setMotorControl(0, 0)
                sleep(1)
            state = 1  # FORWARD
            car.setMotorControl(speed, state)
            logger.info('Direction is forward')
        elif button == 'tr':  # Move backward
            if state == 1:
                car.setMotorControl(0, 0)
                sleep(1)
            state = 2  # BACKWARD
            car.setMotorControl(speed, state)
            logger.info('Direction is backward')
        elif button == 'tl':  # Center the servo
            car.setServoAngle(CENTER_ANGLE)
            logger.info('Centering servo')
    return state, speed, angle

def handle_axis_event(axis, fvalue, car, speed, angle):
    """Handle joystick axis events."""
    axis_states[axis] = fvalue
    logger.info(f"{axis}: {fvalue:.3f}")

    x = axis_states.get('x', 0)
    y = axis_states.get('y', 0)

    if y != 0:  # Adjust speed based on y-axis
        if y > 0:
            speed = max(0, speed - 5)
        else:
            speed = min(car.max_speed, speed + 5)
        car.setMotorControl(speed, car.state)
        logger.info(f'Speed: {speed}')
    elif x != 0:  # Adjust angle based on x-axis
        if x > 0:
            angle = min(car.max_steering, angle + 10)
        else:
            angle = max(car.min_steering, angle - 10)
        car.setServoAngle(angle)
        logger.info(f'Angle: {angle}')
    else:
        car.setMotorControl(car.speed, car.state)
        car.setServoAngle(car.angle)

    return speed, angle

def main():
    """Main function to run the joystick-controlled car."""
    # Check and open Joystick
    check_joystick()
    jsdev = open_joystick()
    get_joystick_info(jsdev)

    # Hocar class initialization
    car = Hocar(INIT_SPEED, CENTER_ANGLE, OBJECT_DISTANCE)
    state = 1  # FORWARD = 1, BACKWARD = 2, STOP = 0
    speed = 50
    angle = CENTER_ANGLE

    # Main event loop
    try:
        while True:
            evbuf = os.read(jsdev.fileno(), 8)

            if evbuf:  # if event happened
                time, value, type, number = struct.unpack('IhBB', evbuf)

                if type & 0x01:  # Button pressed/released
                    button = button_map[number]
                    button_states[button] = value
                    state, speed, angle = handle_button_event(button, value, car, state, speed, angle)

                if type & 0x02:  # Axis move
                    axis = axis_map[number]
                    fvalue = value / 32767.0
                    speed, angle = handle_axis_event(axis, fvalue, car, speed, angle)

    except KeyboardInterrupt:
        logger.info('Ctrl+C pressed, stopping car.')
        car.setMotorControl(0, 0)
        car.setServoAngle(90)
        car.dc_pwm.stop()
        car.servo_pwm.stop()
        GPIO.cleanup()
        sleep(1)

if __name__ == "__main__":
    main()
