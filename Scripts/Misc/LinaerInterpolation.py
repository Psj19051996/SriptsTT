import numpy as np
import matplotlib.pyplot as plt

# Define the linear interpolation function
def linear_interpolate(position_feedback):
    # Define points
    x1, y1 = 80, -100
    x2, y2 = 50, 0
    
    # Linear interpolation formula
    command_output = y1 + (y2 - y1) * (position_feedback - x1) / (x2 - x1)
    return command_output

# Generate a range of position feedback values and calculate command outputs
position_feedback_values = np.linspace(0, 65, 80)  # 100 values from 50 to 80
command_output_values = [linear_interpolate(x) for x in position_feedback_values]

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(position_feedback_values, command_output_values, label="Command Output vs Position Feedback", color="blue")
plt.xlabel("Position Feedback")
plt.ylabel("Command Output")
plt.title("Linear Interpolation: Command Output as Position Feedback Increases")
plt.grid(True)
plt.legend()
plt.show()
