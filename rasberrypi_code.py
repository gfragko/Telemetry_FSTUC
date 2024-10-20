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
            # Example of an incoming packet through the serial monitor
            # "S1:1023,S2:x,S3:x|S1:937,S2:x,S3:x|S1:553,S2:x,S3:x|S1:337,S2:x,S3:x|S1:563,S2:x,S3:x|S1:980,S2:x,S3:x|S1:1023,S2:x,S3:x|S1:762,S2:x,S3:x|S1:370,S2:x,S3:x|S1:368,S2:x,S3:x|"
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                
                #Split data by "|"
                #["S1:1023,S2:x,S3:x","S1:1023,S2:x,S3:x","S1:1023,S2:x,S3:x",.......]
                sensor_values = data.split('|')
                # Split the incoming data by commas 
                #["S1:1023","S2:x","S3:x","S1:1023","S2:x","S3:x","S1:1023","S2:x","S3:x",.......]
                for values in sensor_values:
                    values = values.split(',')
                    
                    if len(values) == 3:#assuming 3 sensors, we need to change according to the application 
                        # Get current timestamp
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")#we can avoid this by adding a clock to each arduino

                        # Write data to file
                        file.write(f"{timestamp},{values[0]},{values[1]},{values[2]}\n")

                        # Flush file to ensure data is saved
                        file.flush()

                        print(f"Logged: {timestamp},{values[0]},{values[1]},{values[2]}")

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Logging stopped.")

    finally:
        # Close serial connection
        ser.close()
