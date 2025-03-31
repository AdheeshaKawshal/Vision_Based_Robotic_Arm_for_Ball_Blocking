import pigpio
import time
import math as mt
from picamera2 import Picamera2
import cv2
import numpy as np
import imutils
# Define servo GPIO pins

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


# Set up PiCamera
picam = Picamera2()
picam.preview_configuration.main.size = (1280, 720)
picam.preview_configuration.main.format = "RGB888"
picam.preview_configuration.align()
picam.configure("preview")
picam.start()

# Ball color range in HSV
greenLower = (5, 150, 150)
greenUpper = (25, 255, 255)

X, Y = [], []  # To store coordinates for prediction

# Allow camera to warm up
time.sleep(2.0)

def linear_regression():
    if len(X) < 2:
        return None, None
    X_mean, Y_mean = sum(X) / len(X), sum(Y) / len(Y)
    numerator = sum((X[i] - X_mean) * (Y[i] - Y_mean) for i in range(len(X)))
    denominator = sum((X[i] - X_mean) ** 2 for i in range(len(X)))
    if denominator == 0:
        return None, None  # Avoid division by zero
    m = numerator / denominator
    b = Y_mean - m * X_mean
    return m, b

def predict_hit_point():
    m, b = linear_regression()
    if m is None or b is None:
        return None
    predicted_x = (370 - b) / m if m != 0 else None  # Assuming the wall is at y=720 (bottom edge)
    return int(predicted_x) if predicted_x is not None and 0 <= predicted_x <= 1280 else None

while True:
    frame = np.fliplr(picam.capture_array())  # Capture and flip if needed
    frame = imutils.resize(frame, width=720)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Create mask for detecting the ball
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    # Find contours
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"] != 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            X.append(center[0])
            Y.append(center[1])
            if len(X) > 20:  # Keep only the last 10 points for prediction
                X.pop(0)
                Y.pop(0)
    # Predict and draw hit point
    hit_x = predict_hit_point()
    if hit_x is not None:
        cv2.circle(frame, (hit_x,370), 10, (255, 0, 0), -1)  # Larger circle
        x_val=53-(hit_x*120/1260)
        print('arm',x_val)
        if (5<x_val and x_val<30):
            
            move_arm(x_val)
            time.sleep(.2) 
        #y_val=center[1]*75/680     
cleanup()
cv2.destroyAllWindows()


