from picamera2 import Picamera2
import cv2
import numpy as np
from collections import deque
from gpiozero import AngularServo
import time
import imutils
import math as mt

# Set up the servo
servo = AngularServo(18, min_angle=0, max_angle=270, min_pulse_width=0.0005, max_pulse_width=0.0025)
WIDTH, HEIGHT = 480,640
X = [] # Independent variable
Y = []  # Dependent variable
# Set up PiCamera
picam = Picamera2()
picam.preview_configuration.main.size = (HEIGHT, WIDTH)  # Lower resolution for faster processing
picam.preview_configuration.main.format = "RGB888"
picam.preview_configuration.align()
picam.configure("preview")
picam.start()

# HSV color range for the ball (adjust as needed)
greenLower = (5,100,100)
greenUpper = (15, 255, 255)

pts = deque(maxlen=10)  # To store previous points (for drawing the path)

time.sleep(2.0)

def linearRgression():
    # Compute means
    global m,b
    X_mean = sum(X) / len(X)
    y_mean = sum(Y) / len(Y)

    # Compute slope (m) using formula: m = Σ((xi - X_mean) * (yi - y_mean)) / Σ((xi - X_mean)^2)
    numerator = sum((X[i] - X_mean) * (Y[i] - y_mean) for i in range(len(X)))
    denominator = sum((X[i] - X_mean) ** 2 for i in range(len(X)))
    m = numerator / denominator

    # Compute intercept (b) using formula: b = y_mean - m * X_mean
    b = y_mean - m * X_mean

# Function to predict new values
def predict():
    yt=Y[len(Y)-1]
    xt=X[len(X)-1]
    s=mt.degrees(mt.atan(m))
    print(' s ',s)
    if m<10 and 0<m: return xt*m-yt
    elif m>-10 and 0>m: return 2*HEIGHT-xt*(-m)-yt
    else: return 0
    #return m * x + b

def getBall_pos():
    fr = picam.capture_array()
    frame = np.fliplr(fr)  # Flip the image horizontally if needed

    # Resize frame for faster processing
    frame = imutils.resize(frame, width=HEIGHT)  # Reduced resolution
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Create a mask for the green color
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=1)  # Reduced erosion
    mask = cv2.dilate(mask, None, iterations=1)  # Reduced dilation

    # Find contours in the mask
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        # Find the largest contour (likely the ball)
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Normalize the coordinates for servo control
        x_val = center[0] * 120 / HEIGHT  # Scale to servo range (0-120)
        y_val = center[1] * 75 / WIDTH   # Scale to servo range (0-75)
        cordinates = (round(x_val, 2), round(y_val, 2))

        # Map x-coordinate to servo angle (range from 0 to 270 degrees)
        movePaddle(cordinates)

        # Draw the contour and center on the frame
        if radius > 10:  # Only process large contours
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)

    # Draw the path of the ball
    for i in range(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue
        thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)  # Dynamic line thickness
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # Show the frame with the ball tracking
    cv2.imshow("Frame", frame)

def movePaddle(cordinates):
    servo.angle = 2 * cordinates[0]


while True:
    # Capture frame  
    getBall_pos()





    # Exit on 'q' key
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
