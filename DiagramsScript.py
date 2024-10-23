import csv
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

# Λίστες για να αποθηκεύσουμε τα δεδομένα
time = []
sensor_1 = []
sensor_2 = []
sensor_3 = []

# Ανάγνωση του CSV αρχείου
with open("multi_sensor_data.csv", 'r') as csvfile: #Βάλε το σωστό file path
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Παράλειψη της κεφαλίδας    drhddhdhbdf
    for row in csvreader:
        time.append(float(row[0])/1000)      # Χρόνος (Time)
        # print("==========================================================")
        sensor_1.append(int(row[1]))    # Τιμές του αισθητήρα 1 (S1)
        sensor_2.append(int(row[2]))    # Τιμές του αισθητήρα 2 (S2)
        sensor_3.append(int(row[3]))    # Τιμές του αισθητήρα 3 (S3)
        
print(time)
print(sensor_1)


# Δημιουργία του γραφήματος
plt.figure(figsize=(10, 6))

# Σχεδιάζουμε τις τιμές των αισθητήρων σε σχέση με τον χρόνο
plt.plot(time, sensor_1, label='Sensor 1')
# plt.plot(time, sensor_2, label='Sensor 2')
# plt.plot(time, sensor_3, label='Sensor 3')


# Προσθήκη ετικετών και τίτλων
plt.xlabel('Time (seconds)')
plt.ylabel('Sensor Values')
plt.title('Sensor Data over Time')
plt.legend()

# Εμφάνιση του γραφήματος
plt.grid(True)
plt.tight_layout()
plt.show()