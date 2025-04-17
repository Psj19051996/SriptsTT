import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

def analyze_and_plot_excel(file_path, x_col, y_col):
    """
    Reads an Excel file, analyzes the requested columns, and plots the data.

    Args:
        file_path (str): Path to the Excel file.
        x_col (str): Name of the column for the X-axis.
        y_col (str): Name of the column for the Y-axis.
    """
    try:
        # Load the Excel file
        data = pd.read_excel(file_path)
        
        # Check if the specified columns exist
        if x_col not in data.columns or y_col not in data.columns:
            print(f"Error: Columns '{x_col}' or '{y_col}' not found in the Excel file.")
            print(f"Available columns: {list(data.columns)}")
            return

        # Extract the required columns
        x_data = data[x_col]
        y_data = data[y_col]

        # Calculate averages
        x_avg = x_data.mean()
        y_avg = y_data.mean()

        print(f"Average of '{x_col}': {x_avg:.2f}")
        print(f"Average of '{y_col}': {y_avg:.2f}")

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(x_data, y_data, marker='o', linestyle='-', color='y')
        plt.axhline(y=y_avg, color='r', linestyle='--', label=f"Average {y_col}: {y_avg:.2f}")
        plt.title(f"{y_col} vs {x_col}")
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.grid(True)
        plt.legend()
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Initialize Tkinter
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window

    # Open a file dialog to select the Excel file
    file_path = filedialog.askopenfilename(
        title="Select an Excel File",
        filetypes=[("Excel Files", "*.xlsx;*.xls")]
    )

    if not file_path:
        print("No file selected. Exiting.")
        return

    # Ask for column names
    x_col = 'Timestamp(ms)'  # Replace with your X-axis column name
    y_col = 'LHS Angle'  # Replace with your Y-axis column name
    #x_col = input("Enter the name of the X-axis column: ").strip()
    #y_col = input("Enter the name of the Y-axis column: ").strip()

    # Analyze and plot the Excel file
    analyze_and_plot_excel(file_path, x_col, y_col)

if __name__ == "__main__":
    main()


