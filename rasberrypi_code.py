import serial
import time

# Initialize serial communication (adjust 'ttyUSB0' as needed)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# File to store data
log_file = '/home/pi/multi_sensor_data.csv'

# Open the file in append mode
with open(log_file, 'a') as file:
    file.write("Timestamp,Potentiometer 1,Potentiometer 2,Temperature Sensor\n")  # Add header

    try:
        while True:
            # Read data from Arduino
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()

                # Split the incoming data by commas (assuming 3 sensors)
                sensor_values = data.split(',')

                if len(sensor_values) == 3:
                    # Get current timestamp
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

                    # Write data to file
                    file.write(f"{timestamp},{sensor_values[0]},{sensor_values[1]},{sensor_values[2]}\n")

                    # Flush file to ensure data is saved
                    file.flush()

                    print(f"Logged: {timestamp},{sensor_values[0]},{sensor_values[1]},{sensor_values[2]}")

            time.sleep(0.5)  # Match the delay in Arduino loop
    except KeyboardInterrupt:
        print("Logging stopped.")

    finally:
        # Close serial connection
        ser.close()
