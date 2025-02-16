import csv
import struct

# Συνάρτηση για μετατροπή δεδομένων σε 16-bit signed integer με little-endian
def convert_sensor_data(sensor_bytes):
    # Μετατροπή σε signed 16-bit integer (little-endian)
    real_value = struct.unpack('<h', sensor_bytes)[0]  # '<h' για signed short (2 bytes) little-endian
    return real_value

# Συνάρτηση για φιλτράρισμα και εκτύπωση δεδομένων από συγκεκριμένα IDs
def filter_and_print_data(csv_file, filter_ids):
    # Διαβάζουμε το αρχείο CSV
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file, delimiter=';')  # Χρησιμοποιούμε ';' ως διαχωριστικό
        
        # Διάβασμα κάθε γραμμής του CSV
        for row in reader:
            # Ελέγχουμε αν το ID είναι στο φίλτρο
            if row['ID'] in filter_ids:
                # Ανακτούμε τα δεδομένα του frame (D0-D7)
                data_bytes = [row[f'D{i}'] for i in range(8)]  # Δημιουργούμε μια λίστα με τα D0-D7
                
                # Μετατροπή των δεδομένων του κάθε αισθητήρα
                sensor_data = []
                for i in range(0, len(data_bytes), 2):
                    # Παίρνουμε κάθε ζεύγος bytes για κάθε αισθητήρα (2 bytes ανά αισθητήρα)
                    sensor_bytes = bytes.fromhex(data_bytes[i]) + bytes.fromhex(data_bytes[i+1])
                    sensor_value = convert_sensor_data(sensor_bytes)
                    sensor_data.append(sensor_value)
                
                # Εκτύπωση των τιμών των αισθητήρων για το συγκεκριμένο ID
                if row['ID'] == '0x101':
                    print(f"ID: {row['ID']} | Potentiometer: {sensor_data[0]}, Ax: {sensor_data[1]}, Ay: {sensor_data[2]}, Az: {sensor_data[3]}")
                elif row['ID'] == '0x201':
                    print(f"ID: {row['ID']} | Potentiometer: {sensor_data[0]}, Gx: {sensor_data[1]}, Gy: {sensor_data[2]}, Gz: {sensor_data[3]}")
                else:
                    print(f"Other ID: {row['ID']} | Sensor 1: {sensor_data[0]}, Sensor 2: {sensor_data[1]}, Sensor 3: {sensor_data[2]}, Sensor 4: {sensor_data[3]}")

# Παράδειγμα φίλτρων για ID (π.χ. να εκτυπώσουμε μόνο τα δεδομένα για ID 0x101 και 0x201)
filter_ids = ['0x101', '0x201']

# Διαβάζουμε και φιλτράρουμε το CSV αρχείο
csv_file = 'can_frames.csv'  # Αντικαταστήστε με το όνομα του αρχείου σας
filter_and_print_data(csv_file, filter_ids)
