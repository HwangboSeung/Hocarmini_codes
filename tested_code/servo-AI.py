import RPi.GPIO as GPIO
import time

# Set up GPIO:
servo_pin = 17  # GPIO pin connected to the servo signal line
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(servo_pin, GPIO.OUT)

# Initialize PWM on the servo pin:
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz frequency, suitable for servo motors

# Function to set servo angle:
def set_servo_angle(angle):
    """
    Sets the servo motor to the specified angle.
    
    Args:
    angle (float): The target angle in degrees.
    """
    duty_cycle = (angle / 18) + 2  # Convert angle to duty cycle
    pwm.start(duty_cycle)
    time.sleep(0.5)  # Wait for the servo to move to the target angle
    pwm.ChangeDutyCycle(0)  # Prevents jitter

try:
    pwm.start(0)
    while True:
        angle = float(input("Enter the steering angle (0 to 180 degrees): "))
        if 0 <= angle <= 180:
            set_servo_angle(angle)
        else:
            print("Angle must be between 0 and 180 degrees.")
except KeyboardInterrupt:
    # Clean up GPIO and PWM on exit
    pwm.stop()
    GPIO.cleanup()
