# Ball Tracking and Path Prediction Robot

## Project Description
This project implements a color-based ball tracking and path prediction system using a Raspberry Pi, PiCamera, and a robotic arm controlled by servos. The system utilizes OpenCV for image processing to detect a colored ball (configured for green in HSV color space), track its movement, and predict its future trajectory to enable the robotic arm to block the ball at a predefined hit point. The robotic arm adjusts its position dynamically based on the predicted path, aiming to intercept or block the ball as it reaches a specific location (e.g., the bottom edge of the camera frame). The project uses the `pigpio` library for precise servo control and linear regression for trajectory prediction, making it ideal for educational purposes, robotics demonstrations, or as a foundation for more advanced automation tasks.

## Repository Contents
- `ball_tracking_robot.py`: Main Python script containing the ball tracking, trajectory prediction, and servo control logic.

## Prerequisites
- Hardware:
  - Raspberry Pi (with PiCamera module)
  - Two servos connected to GPIO pins 18 and 12
  - Robotic arm structure with appropriate linkage lengths (set as 18cm and 20cm in code)
  - Power supply for Raspberry Pi and servos

- Software:
  - Raspberry Pi OS
  - Python 3.x
  - Installed libraries:
    - `picamera2`
    - `opencv-python` (cv2)
    - `numpy`
    - `imutils`
    - `pigpio`

## Installation

### Hardware Setup
1. Connect the servos to the Raspberry Pi's GPIO pins:
   - Servo 1: GPIO 18
   - Servo 2: GPIO 12
   Ensure the servos are powered appropriately and the signal wires are connected to the correct GPIO pins.

2. Attach the PiCamera module to the Raspberry Pi camera port and ensure it is enabled in the Raspberry Pi configuration.

3. Assemble the robotic arm with segments of lengths approximately 18cm and 20cm (adjustable in the code if different). Position the arm so it can reach the area where the ball is expected to be blocked (e.g., near the bottom of the camera frame).
