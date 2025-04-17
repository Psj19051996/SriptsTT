import os
import math
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def calculate_theta(a, b, c):
    """
    Calculates the angle theta using the Law of Cosines.
    """
    if c > a + b or c < abs(a - b):  # Check if the value of c is valid
        return None  # Invalid configuration

    cos_theta = (a**2 + b**2 - c**2) / (2 * a * b)  # Law of Cosines
    cos_theta = max(-1, min(1, cos_theta))  # Ensure cos(theta) is within -1 to 1
    theta_radians = math.acos(cos_theta) - 1.2435409305451417  # Subtract offset
    theta_degrees = math.degrees(theta_radians)  # Convert to degrees
    return theta_degrees  # Return angle in degrees


# Constants
a = 1205.07  # Constant length a
b = 2228.4   # Constant length b


def analyze_and_plot_excel():
    """
    Loads an Excel file, calculates test angles, and plots test angles against Mast Angles.
    """
    try:
        # Open file dialog to select the Excel file
        Tk().withdraw()  # Hide the root Tkinter window
        file_path = askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])

        if not file_path:
            print("No file selected. Operation cancelled.")
            return

        print(f"Selected file: {file_path}")

        # Load the Excel file
        data = pd.read_excel(file_path)

        # Check if necessary columns exist
        if "LHS LVDT" not in data.columns or "Mast Angle" not in data.columns:
            print(f"Error: Required columns 'LHS LVDT' or 'Mast Angle' not found in the file.")
            print(f"Available columns: {list(data.columns)}")
            return

        # Perform calculations using "LHS LVDT" as c
        data["Test Angle"] = data["LHS LVDT"].apply(lambda c: calculate_theta(a, b, c + 2166) if not pd.isnull(c) else None)

        # Filter rows with valid test angles
        valid_data = data.dropna(subset=["Test Angle", "Mast Angle"])

        # Plotting Test Angle vs Mast Angle
        plt.figure(figsize=(10, 6))
        plt.plot(valid_data["Test Angle"], valid_data["Mast Angle"], marker='o', linestyle='-', color='blue', label="Mast Angle vs Test Angle")
        plt.xlabel("Test Angle (degrees)")
        plt.ylabel("Mast Angle (degrees)")
        plt.title("Comparison of Test Angle and Mast Angle")
        plt.grid(True)
        plt.legend()
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")


# Run the function
analyze_and_plot_excel()
