import serial
import time
from datetime import datetime

# Initialize serial communication (adjust 'COM12' as needed)
ser = serial.Serial('COM12', 9600)  # For Windows

# File to store data
log_file = 'multi_sensor_data.csv'

# Open the file in append mode
with open(log_file, 'a') as file:
    file.write("Timestamp,Sensor 1,Sensor 2,Sensor 3\n")  # Add header

    try:
        while True:
            # Read data from Arduino
            # Example of an incoming packet through the serial monitor
           
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                
                #Split data by "|"
                
                sensor_values = data.split('|')
                # Split the incoming data by commas 
                #[["S1:1023","S2:x","S3:x"],"S1:1023","S2:x","S3:x","S1:1023","S2:x","S3:x",.......]
                for values in sensor_values:
                    values = values.split(',')
                    
                    if len(values) == 4:#assuming time and 3 sensors, we need to change according to the application 
                        # Get current timestamp
                        # timestamp = time.strftime("%Y-%m-%d %H:%M:%S")#we can avoid this by adding a clock to each arduino
                        timestamp = values[0]

                        # Write data to file
                        file.write(f"{timestamp},{values[1]},{values[2]},{values[3]}\n")

                        # Flush file to ensure data is saved
                        file.flush()

                        print(f"Logged: {timestamp},{values[1]},{values[2]},{values[3]}")

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Logging stopped.")

    finally:
        # Close serial connection
        ser.close()
