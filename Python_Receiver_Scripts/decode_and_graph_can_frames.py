import csv
import struct
import matplotlib.pyplot as plt

# Function to convert sensor data to 16-bit signed integer with little-endian
def convert_sensor_data(sensor_bytes):
    # Convert to signed 16-bit integer (little-endian)
    real_value = struct.unpack('<h', sensor_bytes)[0]  # '<h' for signed short (2 bytes) little-endian
    return real_value

# Function to filter and plot data from specific IDs
def filter_and_plot_data(input_csv_file, filter_ids):
    # Lists to store data
    potentiometer_values = []
    ax_values = []
    ay_values = []
    az_values = []
    timestamps_potentiometer = []  # For Potentiometer (0x101)
    
    gx_values = []
    gy_values = []
    gz_values = []
    timestamps_gyroscope = []  # For Gyroscope (0x201)

    # Read the CSV file
    with open(input_csv_file, mode='r') as file:
        reader = csv.DictReader(file, delimiter=';')  # Using ';' as delimiter
        
        # Read each row of the CSV
        for row in reader:
            # Check if ID is in the filter list
            if row['ID'] in filter_ids:
                # Extract frame data (D0-D7)
                data_bytes = [row[f'D{i}'] for i in range(8)]  # Create a list with D0-D7
                
                # Convert sensor data
                sensor_data = []
                for i in range(0, len(data_bytes), 2):
                    # Take each pair of bytes for each sensor (2 bytes per sensor)
                    sensor_bytes = bytes.fromhex(data_bytes[i]) + bytes.fromhex(data_bytes[i+1])
                    sensor_value = convert_sensor_data(sensor_bytes)
                    sensor_data.append(sensor_value)
                
                # If ID is '0x101' (Potentiometer), add to corresponding lists
                if row['ID'] == '0x101':
                    print(f"ID: {row['ID']} | Potentiometer: {sensor_data[0]}, Ax: {sensor_data[1]}, Ay: {sensor_data[2]}, Az: {sensor_data[3]}")
                    potentiometer_values.append(sensor_data[0])
                    ax_values.append(sensor_data[1])
                    ay_values.append(sensor_data[2])
                    az_values.append(sensor_data[3])
                    timestamps_potentiometer.append(row['Time'])  # Add timestamp for Potentiometer

                # If ID is '0x201' (Gyroscope), add to corresponding lists
                elif row['ID'] == '0x201':
                    print(f"ID: {row['ID']} | Potentiometer: {sensor_data[0]}, Gx: {sensor_data[1]}, Gy: {sensor_data[2]}, Gz: {sensor_data[3]}")
                    gx_values.append(sensor_data[1])
                    gy_values.append(sensor_data[2])
                    gz_values.append(sensor_data[3])
                    timestamps_gyroscope.append(row['Time'])  # Add timestamp for Gyroscope

    # Ensure timestamps and sensor values have matching lengths
    if len(timestamps_potentiometer) == len(potentiometer_values) and len(timestamps_gyroscope) == len(gx_values):
        # Create plots for both Potentiometer and Gyroscope
        plot_ID_101_data(timestamps_potentiometer, potentiometer_values, ax_values, ay_values, az_values)
        plot_ID_201_data(timestamps_gyroscope, potentiometer_values, gx_values, gy_values, gz_values)
    else:
        print("Error: Mismatch in data dimensions between timestamps and sensor values.")

# Function to create a plot for the Potentiometer (ID 0x101)
def plot_ID_101_data(timestamps, potentiometer_values, ax_values, ay_values, az_values):
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))  # Create 2x2 subplots
    
    # Create plots for each sensor
    axs[0, 0].plot(timestamps, potentiometer_values, label='Potentiometer', color='tab:blue')
    axs[0, 0].set_title('Potentiometer')
    axs[0, 0].set_xlabel('Time')
    axs[0, 0].set_ylabel('Value')
    
    axs[0, 1].plot(timestamps, ax_values, label='Ax', color='tab:orange')
    axs[0, 1].set_title('Ax')
    axs[0, 1].set_xlabel('Time')
    axs[0, 1].set_ylabel('Value')
    
    axs[1, 0].plot(timestamps, ay_values, label='Ay', color='tab:green')
    axs[1, 0].set_title('Ay')
    axs[1, 0].set_xlabel('Time')
    axs[1, 0].set_ylabel('Value')
    
    axs[1, 1].plot(timestamps, az_values, label='Az', color='tab:red')
    axs[1, 1].set_title('Az')
    axs[1, 1].set_xlabel('Time')
    axs[1, 1].set_ylabel('Value')

    # Adjust layout and save the plot as an image
    plt.tight_layout()
    plt.savefig('potentiometer_sensor_data_subplots.png')
    plt.show()

# Function to create a plot for the Gyroscope (ID 0x201)
def plot_ID_201_data(timestamps, potentiometer_values, gx_values, gy_values, gz_values):
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))  # Create 2x2 subplots
    
    # Create plots for each sensor
    axs[0, 0].plot(timestamps, potentiometer_values, label='Potentiometer', color='tab:blue')
    axs[0, 0].set_title('Potentiometer')
    axs[0, 0].set_xlabel('Time')
    axs[0, 0].set_ylabel('Value')
    
    axs[0, 1].plot(timestamps, gx_values, label='Gx', color='tab:orange')
    axs[0, 1].set_title('Gx')
    axs[0, 1].set_xlabel('Time')
    axs[0, 1].set_ylabel('Value')
    
    axs[1, 0].plot(timestamps, gy_values, label='Gy', color='tab:green')
    axs[1, 0].set_title('Gy')
    axs[1, 0].set_xlabel('Time')
    axs[1, 0].set_ylabel('Value')
    
    axs[1, 1].plot(timestamps, gz_values, label='Gz', color='tab:red')
    axs[1, 1].set_title('Gz')
    axs[1, 1].set_xlabel('Time')
    axs[1, 1].set_ylabel('Value')


    # Adjust layout and save the plot as an image
    plt.tight_layout()
    plt.savefig('gyroscope_sensor_data_subplots.png')
    plt.show()

# Example filter for IDs (e.g., to print only data for ID 0x101 and 0x201)
filter_ids = ['0x101', '0x201']

# Define the input file
input_csv_file = 'can_frames.csv'  # Replace with your file name

# Read, filter, and plot data from the CSV file
filter_and_plot_data(input_csv_file, filter_ids)
