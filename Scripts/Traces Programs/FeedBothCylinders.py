import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def analyze_and_plot_excel(x_col1, x_col2, y_col1, y_col2):
    """
    Reads an Excel file (selected by the user), filters invalid rows, 
    and creates two subplots in one figure for the specified columns.

    Args:
        x_col1 (str): Name of the column for the X1-axis.
        x_col2 (str): Name of the column for the X2-axis.
        y_col1 (str): Name of the column for the Y1-axis.
        y_col2 (str): Name of the column for the Y2-axis.

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
        
        # Check if the specified columns exist
        missing_columns = [col for col in [x_col1, x_col2, y_col1, y_col2] if col not in data.columns]
        if missing_columns:
            print(f"Error: Columns {missing_columns} not found in the Excel file.")
            print(f"Available columns: {list(data.columns)}")
            return

        # Filter rows with invalid data
        invalid_rows = data[(data[x_col1].isna()) | (data[x_col2].isna()) | (data[y_col1].isna())]
        filtered_data = data.dropna(subset=[x_col1, x_col2, y_col1,y_col2])

        # Optional: Filter by a value range (customize as needed)
        # filtered_data = filtered_data[(filtered_data[y_col].abs() <= 1000)]

        # Report excluded rows
        if not invalid_rows.empty:
            print(f"Excluded {len(invalid_rows)} rows with invalid data:")
            print(invalid_rows)

        # Extract filtered columns
        x_col1_data = filtered_data[x_col1]
        x_col2_data = filtered_data[x_col2]
        y_col1_data = filtered_data[y_col1]
        y_col2_data = filtered_data[y_col2]

        # Calculate averages
        x_col1_avg = x_col1_data.mean()
        x_col2_avg = x_col2_data.mean()
        y_col1_avg = y_col1_data.mean()
        y_col2_avg = y_col2_data.mean()
        y_col1_max = y_col1_data.max()
        y_col2_max = y_col2_data.max()
        y_col1_min = y_col1_data.min()
        y_col2_min = y_col2_data.min()

        print(f"Average of '{x_col1}': {x_col1_avg:.2f}")
        print(f"Average of '{x_col2}': {x_col2_avg:.2f}")
        print(f"Average of '{y_col1}': {y_col1_avg:.2f}")
        print(f"Average of '{y_col2}': {y_col2_avg:.2f}")
        print(f"Maximum Value of '{y_col1}': {y_col1_max:.2f}")
        print(f"Maximum Value of '{y_col2}': {y_col2_max:.2f}")
        print(f"Minimum Value of '{y_col1}': {y_col1_min:.2f}")
        print(f"Minimum Value of '{y_col2}': {y_col2_min:.2f}")


        # Create subplots
        fig, axs = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

        # Plot 1: X1 vs Y1
        axs[0].plot(x_col1_data, y_col1_data, marker='o', linestyle='-', color='blue', label='Filtered Data')
        axs[0].axhline(y=y_col1_avg, color='red', linestyle='--', label=f"Average {y_col1}: {y_col1_avg:.2f}")
        axs[0].axhline(y=y_col1_max, color='violet', linestyle='--', label=f"Maximum {y_col1}: {y_col1_max:.2f}")
        axs[0].set_title(f"{y_col1} vs {x_col1}")
        axs[0].set_xlabel(x_col1)
        axs[0].set_ylabel(y_col1)
        axs[0].grid(True)
        axs[0].legend()

        # Plot 2: RHS vs Difference
        axs[1].plot(x_col2_data, y_col2_data, marker='x', linestyle='-', color='green', label='Filtered Data')
        axs[1].axhline(y=y_col2_avg, color='red', linestyle='--', label=f"Average {y_col2}: {y_col2_avg:.2f}")
        axs[1].axhline(y=y_col2_max, color='violet', linestyle='--', label=f"Maximum {y_col2}: {y_col2_max:.2f}")
        axs[1].set_title(f"{y_col2} vs {x_col2}")
        axs[1].set_xlabel(x_col2)
        axs[1].set_ylabel(y_col2)
        axs[1].grid(True)
        axs[1].legend()



        # Adjust layout and show the plots
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
x_col1 = 'LHS LVDT'  # Replace with your LHS column name
x_col2 = 'RHS LVDT'  # Replace with your RHS column name
y_col1 = 'DIFFERENCE'  # Replace with your Y-axis column name
y_col2 = 'DIFFERENCE'  # Replace with your Y-axis column name

analyze_and_plot_excel(x_col1, x_col2, y_col1, y_col2)






