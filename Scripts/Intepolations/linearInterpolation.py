import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from scipy.interpolate import interp1d

# Function to get user input
def get_user_values():
    n = int(input("Enter the number of data points: "))
    x_vals = []
    y_vals = []
    
    print("Enter x and y values:")
    for i in range(n):
        x = float(input(f"x[{i+1}]: "))
        y = float(input(f"y[{i+1}]: "))
        x_vals.append(x)
        y_vals.append(y)
    
    return np.array(x_vals), np.array(y_vals)

# Get user inputs
x_data, y_data = get_user_values()

# Sort data to ensure proper interpolation
sorted_indices = np.argsort(x_data)
x_data, y_data = x_data[sorted_indices], y_data[sorted_indices]

# Ensure unique x-values
if len(np.unique(x_data)) != len(x_data):
    print("\nError: Duplicate x-values found. Please enter unique x-values.")
    exit()

# Perform interpolation
interp_func = interp1d(x_data, y_data, kind='linear', fill_value="extrapolate")

# Get interpolation point
x_interp = float(input("Enter the x-value for interpolation: "))
y_interp = interp_func(x_interp)

# Calculate minimum resolution (smallest difference) in both x and y
if len(x_data) > 1:  
    min_x_resolution = np.min(np.diff(np.round(x_data, 5)))  # Min difference in x-values (5 decimal places)
    min_y_resolution = np.min(np.diff(np.round(y_data, 5)))  # Min difference in y-values (5 decimal places)
else:
    min_x_resolution, min_y_resolution = None, None

# Calculate slope (m) and constant (c) for each segment
slopes = []
constants = []
segments = []

print("\nBreakpoints and Equation Parameters (y = mx + c):")
for i in range(len(x_data) - 1):
    x1, x2 = x_data[i], x_data[i+1]
    y1, y2 = y_data[i], y_data[i+1]
    
    m = (y2 - y1) / (x2 - x1)  # Slope
    c = y1 - m * x1  # Constant
    
    slopes.append(m)
    constants.append(c)
    segments.append(f"[{x1}, {x2}]")
    
    print(f"Segment [{x1}, {x2}]: m = {m:.5f}, c = {c:.5f}")

# Display results
print(f"\nInterpolated y-value at x = {x_interp}: {y_interp:.5f}")
if min_x_resolution is not None:
    print(f"Minimum resolution in x-values: {min_x_resolution:.5f}")
    print(f"Minimum resolution in y-values: {min_y_resolution:.5f}")

# Open file save dialog
root = tk.Tk()
root.withdraw()
file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

if file_path:
    # Create DataFrame and save to Excel
    data_dict = {
        "X Values": x_data,
        "Y Values": y_data
    }

    eqn_dict = {
        "Segment": segments,
        "Slope (m)": slopes,
        "Intercept (c)": constants
    }

    # Create Pandas Excel writer
    with pd.ExcelWriter(file_path) as writer:
        pd.DataFrame(data_dict).to_excel(writer, sheet_name="Data Points", index=False)
        pd.DataFrame(eqn_dict).to_excel(writer, sheet_name="Equations", index=False)
        pd.DataFrame({"Interpolated X": [x_interp], "Interpolated Y": [y_interp]}).to_excel(writer, sheet_name="Interpolation", index=False)
        
    print(f"Data successfully saved to {file_path}")

# Plot the data and interpolation point
plt.plot(x_data, y_data, 'bo-', label='Given Data')
plt.scatter(x_interp, y_interp, color='red', label=f'Interpolated ({x_interp:.5f}, {y_interp:.5f})')

# Annotate the slope and constant at each segment
for i in range(len(x_data) - 1):
    mid_x = (x_data[i] + x_data[i+1]) / 2
    mid_y = (y_data[i] + y_data[i+1]) / 2
    plt.text(mid_x, mid_y, f"m={slopes[i]:.2f}\nc={constants[i]:.2f}", fontsize=10, color='green')

plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Linear Interpolation with Breakpoints")
plt.legend()
plt.grid(True)
plt.show()
