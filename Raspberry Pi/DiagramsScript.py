import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV data into a DataFrame
from io import StringIO
df = pd.read_csv("test_rtc.csv")

# Convert the 'Timestamp' column to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Set the 'Timestamp' as the index for plotting
df.set_index('Timestamp', inplace=True)

# Plot the sensor data
# plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Sensor 1'], label='Sensor 1', marker='o')
plt.plot(df.index, df['Sensor 2'], label='Sensor 2', marker='x')
plt.plot(df.index, df['Sensor 3'], label='Sensor 3', marker='s')


print(df['Sensor 1'])


# Adding titles and labels
plt.title('Sensor Values Over Time')
plt.xlabel('Timestamp')
plt.ylabel('Sensor Values')
plt.xticks(rotation=45)
plt.grid()
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()
