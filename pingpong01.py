from picamera2 import Picamera2
import cv2
import numpy as np
from collections import deque
from gpiozero import AngularServo
import time
import imutils

# Set up the servo
servo = AngularServo(18, min_angle=0, max_angle=270, min_pulse_width=0.0005, max_pulse_width=0.0025)

# Set up PiCamera
picam = Picamera2()
picam.preview_configuration.main.size = (640, 480)  # Lower resolution for faster processing
picam.preview_configuration.main.format = "RGB888"
picam.preview_configuration.align()
picam.configure("preview")
picam.start()

# HSV color range for the ball (adjust as needed)
greenLower = (5,100,100)
greenUpper = (15, 255, 255)

pts = deque(maxlen=10)  # To store previous points (for drawing the path)

time.sleep(2.0)

def getBall_pos():
    fr = picam.capture_array()
    frame = np.fliplr(fr)  # Flip the image horizontally if needed

    # Resize frame for faster processing
    frame = imutils.resize(frame, width=640)  # Reduced resolution
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
        x_val = center[0] * 120 / 640  # Scale to servo range (0-120)
        y_val = center[1] * 75 / 480   # Scale to servo range (0-75)
        cordinates = (round(x_val, 2), round(y_val, 2))

        # Map x-coordinate to servo angle (range from 0 to 270 degrees)
        servo.angle = 2 * cordinates[0]

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


while True:
    # Capture frame  
    getBall_pos()




    
    # Exit on 'q' key
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
