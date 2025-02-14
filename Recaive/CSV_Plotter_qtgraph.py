import csv
import pandas as pd
import pyqtgraph as pg
from pyqtgraph.Qt import QtWidgets
from collections import defaultdict
from tkinter import filedialog, Tk
from datetime import datetime

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
        
        # Parse timestamps to datetime
        base_time = None
        
        for row in reader:
            timestamp, sensor_id, *values = row
            
            # Convert timestamp into datetime
            try:
                current_time = datetime.strptime(timestamp, "%H:%M:%S.%f")
                if base_time is None:
                    base_time = current_time  # Set base time to first timestamp
                elapsed_seconds = (current_time - base_time).total_seconds()  # Get elapsed time in seconds
            except ValueError:
                continue  # Skip invalid timestamps

            if sensor_id in sensor_dict:
                sensor_names = sensor_dict[sensor_id]
                for name, value in zip(sensor_names, values):
                    if name != 'NO_SENSOR':
                        try:
                            sensor_data[name]['timestamps'].append(elapsed_seconds)
                            sensor_data[name]['values'].append(float(value))
                        except ValueError:
                            sensor_data[name]['values'].append(value)  # Keep as string if conversion fails
    
    return sensor_data

def plot_all_sensors(sensor_data, labels, title):
    app = QtWidgets.QApplication.instance()  # Χρησιμοποίησε υπάρχον QApplication αν υπάρχει
    if app is None:
        app = QtWidgets.QApplication([])

    win = pg.GraphicsLayoutWidget(title=title)
    win.resize(1000, 600)
    win.show()

    p = win.addPlot(title=title)
    p.showGrid(x=True, y=True)
    p.addLegend()

    p.setLabel("left", "Sensor Values")
    p.setLabel("bottom", "Time (s)")

    colors = ['r', 'g', 'b', 'y', 'm', 'c', 'w']
    
    for i, label in enumerate(labels):
        if label in sensor_data and len(sensor_data[label]['timestamps']) > 0:
            p.plot(sensor_data[label]['timestamps'], sensor_data[label]['values'], 
                   pen=pg.mkPen(colors[i % len(colors)], width=2), name=label)

    QtWidgets.QApplication.instance().exec()

def subplot_all_sensors(sensor_data, labels, title):
    app = QtWidgets.QApplication.instance()  # Use existing QApplication if available
    if app is None:
        app = QtWidgets.QApplication([])

    win = pg.GraphicsLayoutWidget(title=title)
    win.resize(800, 600)
    win.show()
    
    colors = ['r', 'g', 'b', 'y', 'm', 'c', 'w']  # Color palette

    all_timestamps = []
    for label in labels:
        if label in sensor_data:
            all_timestamps.extend(sensor_data[label]['timestamps'])
    
    min_timestamp = min(all_timestamps)
    max_timestamp = max(all_timestamps)
    
    plots = []
    for i, label in enumerate(labels):  # Add index 'i' to access colors
        if label in sensor_data:
            p = win.addPlot(title=label)
            p.plot(sensor_data[label]['timestamps'], sensor_data[label]['values'], pen=pg.mkPen(colors[i % len(colors)], width=2), name=label)
            p.showGrid(x=True, y=True)
            p.setXRange(min_timestamp, max_timestamp)
            plots.append(p)
            win.nextRow()
    
    app.exec()

    
# File selection using Tkinter
root = Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title="Select a CSV file")

if file_path:
    sensor_data = read_csv_and_extract_data(file_path, sensor_dict)
    print("Available Sensors:", sensor_data.keys())

    for label in ['RPM', 'Throttle', 'MAP', 'Intake Air Temp']:
        if label in sensor_data:
            print(f"\n{label} timestamps:", sensor_data[label]['timestamps'][:5])  # Δείξε τα πρώτα 5
            print(f"{label} values:", sensor_data[label]['values'][:5])

    subplot_all_sensors(sensor_data, ['RPM', 'Throttle', '  MAP', 'Intake Air Temp'], 'Sensor Data Over Time')
    #subplot_all_sensors(sensor_data, ['Pot_1', 'Pot_2'], 'Sensor Data Over Time')
    #plot_all_sensors(sensor_data, ['RPM', 'Throttle', 'MAP', 'Intake Air Temp'], 'Sensor Data Over Time')

