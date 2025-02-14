import csv
import matplotlib.pyplot as plt
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import time
import pickle
import matplotlib.dates as mdates
import numpy as np
import datetime


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
    '0x538': ['Brake Pressure'],
    '0x527': ['Lambda Target', 'NO_SENSOR', 'NO_SENSOR', 'NO_SENSOR'],
    '0x542': ['ECU Errors', 'NO_SENSOR', 'NO_SENSOR', 'NO_SENSOR']
}

def read_csv_and_extract_data(file_path, sensor_dict):
    # Initialize storage for sensor data with timestamps
    sensor_data = defaultdict(lambda: {'timestamps': [], 'values': []})
    
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        
        for row in reader:
            timestamp, sensor_id, *values = row
            
            if sensor_id in sensor_dict:
                sensor_names = sensor_dict[sensor_id]
                for name, value in zip(sensor_names, values):
                    if name != 'NO_SENSOR':
                        try:
                            sensor_data[name]['timestamps'].append(timestamp)
                            sensor_data[name]['values'].append(float(value))
                        except ValueError:
                            sensor_data[name]['values'].append(value)  # Keep as string if conversion fails
    
    return sensor_data


def plot_all_sensors(sensor_data, labels, title):
    plt.figure(figsize=(10, 5))
    for label in labels:
        if label in sensor_data:
            plt.plot(sensor_data[label]['timestamps'], sensor_data[label]['values'], label=label)
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title(title)
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()
    
    
# def get_out_path():
    

def plot_sensors_subplots(sensor_data, labels, title):
    num_sensors = len(labels)
    fig, axes = plt.subplots(num_sensors, 1, figsize=(10, 5 * num_sensors), sharex=True)

    if num_sensors == 1:
        axes = [axes]  # Ensure axes is iterable when there's only one sensor
        
    for ax, label in zip(axes, labels):
        if label in sensor_data:
            # ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=1))  # Show label every 10 minutes
            ax.plot(sensor_data[label]['timestamps'], sensor_data[label]['values'], label=label)
            ax.set_ylabel('Value')
            ax.legend()
            # ax.grid(True)
            ax.grid(False)

    axes[-1].set_xlabel('Time')  # Set xlabel only for the last subplot
    fig.suptitle(title)
    plt.xticks(rotation=45)
    out_path = r"Out\out1.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.show()


#========================================================================================================
root = tk.Tk()
root.withdraw()  # Hide the main window
# Open file explorer and select a file
file_path = filedialog.askopenfilename(title="Select a file")
df = pd.read_csv(file_path)
#--------------------------------------------------------------------------------------------------------



sensor_data = read_csv_and_extract_data(file_path, sensor_dict)
plot_all_sensors(sensor_data, ['RPM', 'Throttle', 'MAP', 'Intake Air Temp'], 'RPM / Throttle / MAP / Intake Air Temp over Time')


# 1) RPM / Throttle / MAP / Intake Air Temptext="Processing...", color="yellow", spinner="dots", side="right"
# with yaspin(text="Plotting->RPM/Throttle/MAP/Intake Air Temp", color="yellow", spinner="line")as sp:
#     plot_sensors_subplots(sensor_data, ['RPM', 'Throttle', 'MAP', 'Intake Air Temp'], 'RPM / Throttle / MAP / Intake Air Temp over Time')
#     sp.ok("✔ Done!") 
# 2) RPM / Gear / Battery Voltage
# with yaspin(text="Plotting-> RPM / Gear / Battery Voltage", color="yellow", spinner="dots"):
#     plot_sensors_subplots(sensor_data, ['RPM', 'Gear', 'Battery Voltage'], 'RPM / Gear / Battery Voltage over Time')

# # 3) Lambda / Lambda A / Ignition Angle / Ignition Cut / Fuel Cut / Lambda Corr A
# with yaspin(text="Plotting-> Lambda / Lambda A / Ignition Angle / Ignition Cut / Fuel Cut / Lambda Corr A", color="yellow", spinner="dots"):
#     plot_sensors_subplots(sensor_data, ['Lambda', 'Lambda A', 'Ignition Angle', 'Ignition Cut', 'Fuel Cut', 'Lambda Corr A'], 'Lambda-related Parameters over Time')
