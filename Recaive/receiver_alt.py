import can
import subprocess
import struct
import matplotlib.pyplot as plt
import time
from datetime import datetime
import csv

# sudo ip link set can0 up type can bitrate 1000000
# sudo ip link set can0 down
# ip link show can0
# ip -details link show can0
# sudo raspi-config

def decode_message_101_201(arbitration_id, data_bytes_hex):
    sensor_data = []
    for i in range(0, len(data_bytes_hex), 4):
        sensor_bytes = bytes.fromhex(data_bytes_hex[i:i+4])
        val = struct.unpack('<h', sensor_bytes)[0]
        sensor_data.append(val)

    if arbitration_id == 0x101:
        decoded = {
            'Potentiometer': sensor_data[0],
            'Ax': sensor_data[1],
            'Ay': sensor_data[2],
            'Az': sensor_data[3]
        }
    elif arbitration_id == 0x201:
        decoded = {
            'Potentiometer': sensor_data[0],
            'Gx': sensor_data[1],
            'Gy': sensor_data[2],
            'Gz': sensor_data[3]
        }
    else:
        decoded = {
            'UnknownSensor1': sensor_data[0],
            'UnknownSensor2': sensor_data[1],
            'UnknownSensor3': sensor_data[2],
            'UnknownSensor4': sensor_data[3]
        }
    return decoded

def decode_message_ecu(can_id, data):
    """
    Παράδειγμα λογικής από το script 2 (decode_ecu_message).
    can_id: ακέραιος (π.χ. 0x520)
    data: raw bytes (π.χ. b'\x00\x7A\x01\x00...')
    Επιστρέφει ένα dict με τα αποκωδικοποιημένα στοιχεία.
    """
    sensor_values = {}
    try:
        if can_id == 0x520:
            if len(data) >= 8:
                rpm, = struct.unpack_from('<h', data, 0)
                throttle, = struct.unpack_from('<h', data, 2)
                map_val, = struct.unpack_from('<h', data, 4)
                lambda_val, = struct.unpack_from('<h', data, 6)

                sensor_values['RPM'] = rpm
                sensor_values['Throttle'] = round(throttle * 0.1, 1)
                sensor_values['MAP'] = round(map_val * 0.1, 1)
                sensor_values['Lambda'] = round(lambda_val * 0.001, 3)
                
        elif can_id == 0x521:
            if len(data) >= 8:
                lambda_a, = struct.unpack_from('<h', data, 0)
                ignition_angle, = struct.unpack_from('<h', data, 4)
                ignition_cut, = struct.unpack_from('<h', data, 6)

                sensor_values['Lambd A'] = round(lambda_a * 0.001,3)                                                                                                                                                                                                                                                         
                sensor_values['Ignition Angle'] = round(ignition_angle * 0.1, 1)
                sensor_values['Ignition Cut'] = ignition_cut
        elif can_id == 0x522:
            if len(data) >= 8:
                fuel_cut, = struct.unpack_from('<h', data, 4)
                vehicle_speed, = struct.unpack_from('<h', data, 6)

                sensor_values['Fuel Cut'] = fuel_cut
                sensor_values['Vehicle Speed'] = round(vehicle_speed * 0.1, 1)
        elif can_id == 0x524:
            if len(data) >= 4:
                lambda_corr_a, = struct.unpack_from('<h', data, 2)
                sensor_values['Lambda Corr A'] = round(lambda_corr_a * 0.1, 1)
        elif can_id == 0x530:
            if len(data) >= 8:
                batt_voltage, = struct.unpack_from('<h', data, 0)
                intake_air_temp, = struct.unpack_from('<h', data, 4)
                coolant_temp, = struct.unpack_from('<h', data, 6)

                sensor_values['Battery Voltage'] = round(batt_voltage * 0.01, 2)
                sensor_values['Intake Air Temp'] = round(intake_air_temp * 0.1, 1)
                sensor_values['Coolant Temp'] = round(coolant_temp * 0.1, 1)
        elif can_id == 0x536:
            if len(data) >= 8:
                gear, = struct.unpack_from('<h', data, 0)
                oil_pressure, = struct.unpack_from('<h', data, 4)
                oil_temp, = struct.unpack_from('<h', data, 6)

                sensor_values['Gear'] = gear
                sensor_values['Oil Pressure'] = round(oil_pressure * 0.001, 1)
                sensor_values['Oil Temp'] = round(oil_temp * 0.1, 1)
        elif can_id == 0x537:
            if len(data) >= 6:
                coolant_pressure, = struct.unpack_from('<h', data, 4)
                sensor_values['Coolant Pressure'] = round(coolant_pressure * 0.001, 1)
        elif can_id == 0x527:
            if len(data) >= 8:
                lambda_target, = struct.unpack_from('<h', data, 6)
                sensor_values['Lambda Target'] = round(lambda_target * 0.001, 3)
        elif can_id == 0x542:
            if len(data) >= 6:
                ecu_errors, = struct.unpack_from('<h', data, 4)
                sensor_values['ECU Errors'] = ecu_errors
        else:
            # Αν δεν αναγνωρίζουμε το ID, επέστρεψε απλά raw data
            sensor_values['Unknown'] = [f"0x{b:02X}" for b in data]
    except struct.error as e:
        sensor_values['Error'] = f"Struct error: {e}"

    return sensor_values

def unified_decode(can_id, data):
    """
    Ενιαία συνάρτηση που αποφασίζει αν πρόκειται για 0x101/0x201 (script 1) ή για ECU (script 2).
    Επιστρέφει dict με τα δεδομένα.
    """
    
    can_ids = [0x101, 0x201, 0x520, 0x521, 0x522, 0x524, 0x530, 0x536, 0x537, 0x527, 0x542]

    if can_id in [0x101, 0x201]:
        # Εδώ το data υποθέτουμε ότι είναι ήδη bytes. Στο script1 όμως ήθελες data.hex().
        # Για συνέπεια, μετατρέπουμε σε hex κι εφαρμόζουμε decode_message_101_201.
        data_hex = data.hex()  # bytes -> "AB12..."
        return decode_message_101_201(can_id, data_hex)
    elif can_id in can_ids:
        # Χειριζόμαστε το ECU script
        return decode_message_ecu(can_id, data)
    else: 
        return


def print_and_save_sensor_data(id,data,csv_writer):
    # Μετατροπή των δεδομένων του κάθε αισθητήρα
    real_time_stamp = time.strftime('%H:%M:%S') + f".{int(time.time() * 1000) % 1000:03d}"  # HH:MM:SS.mmm
    sensor_dicts = unified_decode(id, data)
    
    text = f"[{real_time_stamp}] ID: 0x{id:X} -> "

    keys = []
    sensor_data = []
    for key,value in sensor_dicts.items():
        keys.append(key)
        sensor_data.append(value)
        text += f"{key}: {value} | "

    while len(keys) < 4:
        keys.append(0)
        sensor_data.append(0)
    
    print(text)
    # print(f"[{real_time_stamp}] ID: 0x{id:X} | {key[0]}: {sensor_data[0]}, {key[1]}: {sensor_data[1]}, {key[2]}: {sensor_data[2]}, {key[3]}: {sensor_data[3]}")
    csv_writer.writerow([f"{real_time_stamp}", f"0x{id:X}", f"{sensor_data [0]}", f"{sensor_data [1]}", f"{sensor_data [2]}", f"{sensor_data [3]}"])
    
    
def receive_can_messages(bus,channel,csv_writer):
    """Receives and prints CAN messages with a specific ID."""

    print(f"Listening for CAN IDs on {channel}...")
    can_ids = [0x101, 0x201, 0x520, 0x521, 0x522, 0x524, 0x530, 0x536, 0x537, 0x527, 0x542]

    try:
        while True:
            message = bus.recv() # Receive message
            if message.arbitration_id in can_ids:
                print_and_save_sensor_data(message.arbitration_id, message.data, csv_writer)
            
            # time.sleep(0.02)
            
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        bus.shutdown()


if __name__ == "__main__":

    now = datetime.now()
    csv_filename = "content//"+now.strftime("%Y-%m-%d_%H.%M.%S")+".csv"
    channel="can0"
    bitrate=500000

    # Ρύθμιση interface
    subprocess.run(['sudo', 'ip', 'link', 'set', channel, 'down'])
    subprocess.run(['sudo', 'ip', 'link', 'set', channel, 'up', 'type', 'can', 'bitrate', str(bitrate)])
    bus = can.interface.Bus(channel=channel, bustype="socketcan")

    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        # Επικεφαλίδες στηλών
        writer.writerow(["Timestamp", "ID", "Sensor1", "Sensor2", "Sensor3", "Sensor4"])
        receive_can_messages(bus,channel,writer)
