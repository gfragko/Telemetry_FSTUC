import pandas as pd
import matplotlib.pyplot as plt

# Define the CSV data as a string (you can also read from a file)
data = """Timestamp,Sensor 1,Sensor 2,Sensor 3
2024-10-21 10:32:59.712479,1023,998,968
2024-10-21 10:32:59.713479,1023,1000,978
2024-10-21 10:32:59.713479,1023,1000,982
2024-10-21 10:32:59.714479,1023,1000,984
2024-10-21 10:32:59.716593,843,887,912
2024-10-21 10:32:59.717479,734,774,815
2024-10-21 10:32:59.717479,734,732,754
2024-10-21 10:32:59.718479,733,720,726
2024-10-21 10:33:00.722035,465,537,592
2024-10-21 10:33:00.723037,286,361,435
2024-10-21 10:33:00.723037,233,272,325
2024-10-21 10:33:00.724037,233,245,272
2024-10-21 10:33:00.725036,224,237,249
2024-10-21 10:33:00.725036,87,144,180
2024-10-21 10:33:00.726037,0,72,116
2024-10-21 10:33:00.726037,0,63,95
2024-10-21 10:33:00.727038,0,58,87
2024-10-21 10:33:00.728036,0,60,86
2024-10-21 10:33:01.731965,0,72,98
2024-10-21 10:33:01.732961,0,59,87
2024-10-21 10:33:01.732961,0,61,87
2024-10-21 10:33:01.732961,0,61,87
2024-10-21 10:33:01.733966,0,64,89
2024-10-21 10:33:01.734407,0,61,87
2024-10-21 10:33:01.734407,90,115,120
2024-10-21 10:33:01.734915,211,200,183
"""

# Read the CSV data into a DataFrame
from io import StringIO
df = pd.read_csv(StringIO(data))

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
