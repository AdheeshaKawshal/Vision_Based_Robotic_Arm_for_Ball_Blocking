import pigpio
import time
import math as mt

# Define GPIO pins for the servos
SERVO1_PIN, SERVO2_PIN = 18, 12  # GPIO pins for Servo 1 and Servo 2

# Initialize pigpio library
pi = pigpio.pi()
if not pi.connected:
    exit("Failed to connect to pigpio daemon.")

def set_angle(pwm_pin, angle):
    """Convert angle to PWM pulse width and send signal."""
    angle = max(20, min(180, angle))  # Ensure angle range
    pulse_width = int((angle / 180.0) * 2000 + 500)  # Map 0-180° to 500-2500µs
    pi.set_servo_pulsewidth(pwm_pin, pulse_width)

def set_angle_simultaneously(angle1, angle2):
    """Move both servos simultaneously to given angles."""
    set_angle(SERVO1_PIN, angle1)
    set_angle(SERVO2_PIN, angle2)

def move_arm(x):
    """Calculate servo angles based on x-coordinate and move servos."""
    l1, l2 = 18, 20  # Arm segment lengths
    
    if x <= 0 or x > (l1 + l2):  # Prevent invalid calculations
        print("Invalid x-coordinate")
        return
    
    angleF = mt.acos((pow(l1,2) + pow(x,2 )- pow(l2,2)) / (2 * x * l1))
    angleG = mt.acos((pow(l2,2) + pow(x,2 )- pow(l1,2) ) / (2 * x * l2))
    
    alpha = mt.degrees(angleF)
    theta = mt.degrees(angleG)
    
    print(f"Moving servos to angles: alpha={alpha}, theta={theta}")
    set_angle_simultaneously(alpha - 10, alpha + theta + 20)
    time.sleep(0.2)  # Small delay for movement

def cleanup():
    """Stops PWM signals and releases GPIO resources."""
    pi.set_servo_pulsewidth(SERVO1_PIN, 0)
    pi.set_servo_pulsewidth(SERVO2_PIN, 0)
    pi.stop()

# Example movement
move_arm(30)
cleanup()
