# Smart-PongBot
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
