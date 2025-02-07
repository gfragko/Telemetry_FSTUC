import pandas as pd
import matplotlib.pyplot as plt
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

# ============================================================================
sensor_dict = {
    '0x101': ['Pot_1', 'ax', 'ay', 'az'],
    '0x201': ['Pot_2', 'gx', 'gy', 'gz'],
    '0x520': ['RPM', 'Throttle', 'MAP', 'Lambda'],
    '0x521': ['Lambda A', 'Ignition Angle', 'Ignition Cut', 'NO_SENSOR'],
    '0x522': ['Fuel Cut', 'Vehicle Speed', 'NO_SENSOR', 'NO_SENSOR'],
    '0x524': ['Lambda Corr A', 'NO_SENSOR', 'NO_SENSOR', 'NO_SENSOR'],
    '0x530': ['Battery Voltage', 'Intake Air Temp', 'Coolant Temp', 'NO_SENSOR'],
    '0x536': ['Gear', 'Oil Pressure', 'Oil Temp', 'NO_SENSOR'],
    '0x537': ['Coolant Pressure', 'NO_SENSOR', 'NO_SENSOR', 'NO_SENSOR'],
    '0x527': ['Lambda Target', 'NO_SENSOR', 'NO_SENSOR', 'NO_SENSOR'],
    '0x542': ['ECU Errors', 'NO_SENSOR', 'NO_SENSOR', 'NO_SENSOR']
}
# ============================================================================


# Load CSV file into a pandas DataFrame

# Create a hidden root window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Open file explorer and select a file
file_path = filedialog.askopenfilename(title="Select a file")
df = pd.read_csv(file_path)

# Convert 'Timestamp' to datetime format for easier plotting
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%H:%M:%S.%f')

# Get the list of unique CAN IDs
can_ids = df['ID'].unique()

plots_folder_name = "CSV_PLOTS "+datetime.now().strftime("%H-%M")
dir_name = Path(plots_folder_name)
# Create the directory if it doesnt exist
dir_name.mkdir(parents=True, exist_ok=True)

# Plot each sensor for each CAN ID
for can_id in can_ids:
    # Filter data for the current CAN ID
    filtered_data = df[df['ID'] == can_id]
    sensor_names = sensor_dict[can_id]
    print("For can id-> ", can_id," i am getting->",sensor_names)

    # Plotting the sensors for the current CAN ID
    plt.figure(figsize=(10, 6))
    plt.plot(filtered_data['Timestamp'], filtered_data['Sensor1'], label=sensor_names[0])
    plt.plot(filtered_data['Timestamp'], filtered_data['Sensor2'], label=sensor_names[1])
    plt.plot(filtered_data['Timestamp'], filtered_data['Sensor3'], label=sensor_names[2])
    plt.plot(filtered_data['Timestamp'], filtered_data['Sensor4'], label=sensor_names[3])
    
    # Customize plot
    plt.title(f"Sensor Data for CAN ID: {can_id}")
    plt.xlabel('Timestamp')
    plt.ylabel('Sensor Values')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    # Show plot
    plot_path = os.path.join(plots_folder_name, can_id+"_plot.png")
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.show()
    # Directory name

    
