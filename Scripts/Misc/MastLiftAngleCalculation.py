import os
import math
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename


def calculate_theta(a, b, c):
    # Check if the value of c is within the valid range for this geometry
    if c > a + b or c < abs(a - b):
        return None  # Invalid configuration
    
    # Calculate cos(theta) using the Law of Cosines
    cos_theta = (a**2 + b**2 - c**2) / (2 * a * b)
    
    # Ensure cos(theta) is within the valid range of -1 to 1 due to floating-point precision
    cos_theta = max(-1, min(1, cos_theta))
    
    # Calculate the angle in radians and adjust with the offset
    theta_radians = math.acos(cos_theta) - 1.2435409305451417
    
    # Convert to degrees (optional)
    theta_degrees = math.degrees(theta_radians)
    
    return theta_radians, theta_degrees

# Constants
a = 1205.07  # constant length a
b = 2228.4   # constant length b

# Range of rPos from 0 to 1250
rPos_values = list(range(0, 1251))
angles_theeta = []
angles_degrees = []
data_points = []

for rPos in rPos_values:
    c = rPos + 2166  # Calculate the cylinder length
    result = calculate_theta(a, b, c)
    
    if result:
        theta_radians, theta_degrees = result
        angles_theeta.append(theta_radians)
        angles_degrees.append(theta_degrees)
        data_points.append((rPos, theta_radians, theta_degrees))
    else:
        angles_theeta.append(None)
        angles_degrees.append(None)  # Append None for invalid configurations
        data_points.append((rPos, None, None))

df = pd.DataFrame(data_points, columns=["rPos (mm)", "Angle (radians)", "Angle (degrees)"])

# Prompt user for save location
Tk().withdraw()  # Hide the root Tkinter window
save_path = asksaveasfilename(
    defaultextension=".xlsx",
    filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
    title="Save Excel File"
)

if save_path:  # If the user selects a file
    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Save the DataFrame to Excel
    with pd.ExcelWriter(save_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Angle_vs_rPos")

    print(f"Excel file saved at: {save_path}")
else:
    print("Save operation was canceled.")


# Plotting
plt.figure(figsize=(10, 6))
plt.plot(rPos_values, angles_degrees, label="Angle (degrees)", color="blue")
plt.xlabel("rPos (mm)")
plt.ylabel("Angle (degrees)")
plt.title("Variation of Angle with rPos")
plt.grid(True)
plt.legend()
plt.show()
