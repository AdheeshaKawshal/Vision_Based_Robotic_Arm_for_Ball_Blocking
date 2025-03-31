# Ball Tracking and Path Prediction Robot

## Project Description
This project implements a color-based ball tracking and path prediction system using a Raspberry Pi, PiCamera, and robotic arm controlled by servos. The system uses OpenCV for image processing to detect a colored ball (configured for green in HSV color space), track its movement, and predict its future path to control a robotic arm. The robotic arm adjusts its position based on the predicted hit point of the ball, aiming to intercept or follow the ball's trajectory. The project utilizes the `pigpio` library for precise servo control and linear regression for path prediction, making it suitable for educational purposes, robotics demonstrations, or as a base for more complex automation tasks.

## Repository Contents
- `ball_tracking_robot.py`: Main Python script containing the ball tracking, path prediction, and servo control logic.

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

3. Assemble the robotic arm with segments of lengths approximately 18cm and 20cm (adjustable in the code if different).

### Software Setup
1. Update and upgrade your Raspberry Pi:

   ```bash
   sudo apt update && sudo apt upgrade -y
