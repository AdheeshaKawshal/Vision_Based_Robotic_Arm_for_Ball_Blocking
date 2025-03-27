import math as mt
import matplotlib.pyplot as plt
import numpy as np

# Constants for the robotic arm (adjust these based on your setup)
l1 = 5.0  # Length of the first arm segment
l2 = 5.0  # Length of the second arm segment
h = 5   # Height or offset parameter  # Normal distance or offset parameter

# Modified moveArm function to compute alpha and theta
def moveArm(coordinates):
    x = coordinates[0]
    # y = coordinates[1]  # Not used in the current formula, but included for completeness
    angelF = mt.acos((l1**2 + x**2 - l2**2) / (2 * x* l1))
    # Compute theta
    angelG = mt.acos((l2**2 + x**2 - l1**2) / (2 * x* l2))
    # Convert to degrees
    alpha = mt.degrees(angelG)
    theta = mt.degrees(angelF)
    print(x / mt.sqrt(x + h**2))
    return alpha, theta

# Generate a range of x values
x_values = np.linspace(0, 5, 100)  # x from 0 to 5, 100 points
alpha_values = []
theta_values = []

# Compute alpha and theta for each x
for x in x_values:
    coordinates = [x, 0]  # y is set to 0 since it's not used
    alpha, theta = moveArm(coordinates)
    alpha_values.append(alpha)
    theta_values.append(theta)

# Create the plots
plt.figure(figsize=(10, 8))

# Plot x vs alpha
plt.subplot(2, 1, 1)
plt.plot(x_values, alpha_values, label='Alpha vs x', color='blue')
plt.xlabel('x')
plt.ylabel('Alpha (degrees)')
plt.title('x vs Alpha')
plt.grid(True)
plt.legend()

# Plot x vs theta
plt.subplot(2, 1, 2)
plt.plot(x_values, theta_values, label='Theta vs x', color='red')
plt.xlabel('x')
plt.ylabel('Theta (degrees)')
plt.title('x vs Theta')
plt.grid(True)
plt.legend()

# Adjust layout and display the plots
plt.tight_layout()
plt.show()