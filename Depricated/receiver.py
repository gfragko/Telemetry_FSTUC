import can
import subprocess
import struct
import matplotlib.pyplot as plt
import time
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

                sensor_values['Lambda A'] = round(lambda_a * 0.001,3)  
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
    if can_id in [0x101, 0x201]:
        # Εδώ το data υποθέτουμε ότι είναι ήδη bytes. Στο script1 όμως ήθελες data.hex().
        # Για συνέπεια, μετατρέπουμε σε hex κι εφαρμόζουμε decode_message_101_201.
        data_hex = data.hex()  # bytes -> "AB12..."
        return decode_message_101_201(can_id, data_hex)
    else:
        # Χειριζόμαστε το ECU script
        return decode_message_ecu(can_id, data)


def convert_sensor_data(sensor_bytes):
# Μετατροπή σε signed 16-bit integer (little-endian)
    real_value = struct.unpack('<h', sensor_bytes)[0] # '<h' για signed short (2 bytes) little-endian
    return real_value

def print_sensor_data(id,data_bytes):
    # Μετατροπή των δεδομένων του κάθε αισθητήρα
    sensor_data = []
    for i in range(0, len(data_bytes), 4):
    # Παίρνουμε κάθε ζεύγος bytes για κάθε αισθητήρα (2 bytes ανά αισθητήρα)
        sensor_bytes = bytes.fromhex(data_bytes[i:i+4])
        sensor_value = convert_sensor_data(sensor_bytes)
        sensor_data.append(sensor_value)
    
    current_time = time.time()
    real_time_stamp = time.strftime('%H:%M:%S') + f".{int(time.time() * 1000) % 1000:03d}"  # HH:MM:SS.mmm
    # Εκτύπωση των τιμών των αισθητήρων για το συγκεκριμένο ID
    if id == 0x101:
        print(f"[{real_time_stamp}] ID: 0x{id:X} | Potentiometer: {sensor_data[0]}, Ax: {sensor_data[1]}, Ay: {sensor_data[2]}, Az: {sensor_data[3]}")
    elif id == 0x201:
        print(f"[{real_time_stamp}] ID: 0x{id:X} | Potentiometer: {sensor_data[0]}, Gx: {sensor_data[1]}, Gy: {sensor_data[2]}, Gz: {sensor_data[3]}")
    else:
        print(f"[{real_time_stamp}] Other ID: 0x{id:X} | Sensor 1: {sensor_data[0]}, Sensor 2: {sensor_data[1]}, Sensor 3: {sensor_data[2]}, Sensor 4: {sensor_data[3]}")


def receive_filtered_can_messages(channel="can0"):
    """Receives and prints CAN messages with a specific ID."""
    #subprocess.run(['sudo', 'modprobe', 'mcp251x'])
    #subprocess.run(['sudo', 'modprobe', 'can_dev'])
    subprocess.run(['sudo', 'ip', 'link', 'set', 'can0', 'down'])
    subprocess.run(['sudo', 'ip', 'link', 'set', 'can0', 'up', 'type', 'can', 'bitrate', '500000'])
    bus = can.interface.Bus(channel=channel, bustype="socketcan")

    print(f"Listening for CAN IDs 0x101 and 0x201 on {channel}...")
    can_ids = [0x101, 0x201]

    try:
        while True:
            message = bus.recv() # Receive message
            for id in can_ids:
                if message.arbitration_id == id:
                    #print(f"Received: ID=0x{message.arbitration_id:X}, Data={message.data.hex()}")
                    print_sensor_data(message.arbitration_id, message.data.hex())
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        bus.shutdown()

# ------------------------------------------------------------------
#                     *** 2) ΝΕΕΣ ΣΥΝΑΡΤΗΣΕΙΣ ***
# ------------------------------------------------------------------
def parse_sensor_data(data_hex):
    """
    Διαβάζει το 'data_hex' (π.χ. '0F1A2B3C...') σε ομάδες των 4 hex
    χαρακτήρων (2 bytes) και επιστρέφει λίστα από signed 16-bit τιμές.
    """
    sensor_values = []
    for i in range(0, len(data_hex), 4):
        # Παίρνουμε 4 χαρακτήρες κάθε φορά (π.χ. '0F1A')
        two_bytes = bytes.fromhex(data_hex[i:i+4])
        # Μετατρέπουμε σε signed 16-bit (little-endian)
        val = struct.unpack('<h', two_bytes)[0]
        sensor_values.append(val)
    return sensor_values

def live_plot_can(channel="can0", bitrate=500000):
    """
    Δημιουργεί 2 Figures:
      - Figure 1: ID=0x101
         * 2 subplots:
             (α) μόνο Pot
             (β) Ax, Ay, Az στην ίδια γραφική παράσταση
      - Figure 2: ID=0x201
         * 2 subplots:
             (α) μόνο Pot
             (β) Gx, Gy, Gz στην ίδια γραφική παράσταση
    Χρησιμοποιεί draining λογική (non-blocking recv) για ελάχιστο lag.
    """

    # 1) Ρύθμιση του CAN interface
    subprocess.run(['sudo', 'ip', 'link', 'set', channel, 'down'])
    subprocess.run(['sudo', 'ip', 'link', 'set', channel, 'up', 'type', 'can', 'bitrate', str(bitrate)])
    bus = can.interface.Bus(channel=channel, bustype="socketcan")

    can_id_101 = 0x101
    can_id_201 = 0x201

    # 2) FIGURE για ID=0x101
    # --------------------------------------------------------
    fig101, (ax101_pot, ax101_3axes) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    fig101.suptitle("ID = 0x101", fontsize=14)

    # (α) Μόνο Pot
    ax101_pot.set_ylabel("Pot(101)")
    ax101_pot.grid(True)
    line_pot_101, = ax101_pot.plot([], [], label='Pot(101)', color='blue')

    # (β) Ax, Ay, Az στο ίδιο subplot
    ax101_3axes.set_ylabel("Ax / Ay / Az")
    ax101_3axes.set_xlabel("Time (s)")
    ax101_3axes.grid(True)
    line_ax_101, = ax101_3axes.plot([], [], label='Ax(101)', color='orange')
    line_ay_101, = ax101_3axes.plot([], [], label='Ay(101)', color='green')
    line_az_101, = ax101_3axes.plot([], [], label='Az(101)', color='red')
    ax101_3axes.legend()

    # Λίστες δεδομένων χρόνου & τιμών
    t_101 = []
    pot_101 = []
    ax_101_list = []
    ay_101_list = []
    az_101_list = []

    # 3) FIGURE για ID=0x201
    # --------------------------------------------------------
    fig201, (ax201_pot, ax201_3axes) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    fig201.suptitle("ID = 0x201", fontsize=14)

    # (α) Μόνο Pot
    ax201_pot.set_ylabel("Pot(201)")
    ax201_pot.grid(True)
    line_pot_201, = ax201_pot.plot([], [], label='Pot(201)', color='blue')

    # (β) Gx, Gy, Gz στο ίδιο subplot
    ax201_3axes.set_ylabel("Gx / Gy / Gz")
    ax201_3axes.set_xlabel("Time (s)")
    ax201_3axes.grid(True)
    line_gx_201, = ax201_3axes.plot([], [], label='Gx(201)', color='orange')
    line_gy_201, = ax201_3axes.plot([], [], label='Gy(201)', color='green')
    line_gz_201, = ax201_3axes.plot([], [], label='Gz(201)', color='red')
    ax201_3axes.legend()

    # Λίστες δεδομένων χρόνου & τιμών
    t_201 = []
    pot_201 = []
    gx_201_list = []
    gy_201_list = []
    gz_201_list = []

    # --------------------------------------------------------
    plt.ion()
    start_time = time.time()

    print(f"Live plotting for ID=0x101 and ID=0x201 on {channel} (bitrate={bitrate})")
    print("Πατήστε Ctrl+C για διακοπή.\n")

    PLOT_INTERVAL = 0.000001  # σχεδίαση ~20 φορές/δευτ.
    last_plot_time = time.time()

    try:
        while True:
            # 1) Διάβασε ΟΛΑ τα διαθέσιμα μηνύματα (drain queue)
            new_msgs = []
            while True:
                msg = bus.recv(timeout=0.0)
                if msg is None:
                    break
                new_msgs.append(msg)

            # 2) Επεξεργασία νέων μηνυμάτων
            for msg in new_msgs:
                # -- ID=0x101
                if msg.arbitration_id == can_id_101:
                    data_list = parse_sensor_data(msg.data.hex())
                    current_time = time.time() - start_time
                    # data_list: [Pot, Ax, Ay, Az]
                    t_101.append(current_time)
                    pot_101.append(data_list[0])
                    ax_101_list.append(data_list[1])
                    ay_101_list.append(data_list[2])
                    az_101_list.append(data_list[3])

                    # Ενημέρωση γραμμών (δεν σχεδιάζουμε ακόμα, το αφήνουμε για μετά)
                    line_pot_101.set_xdata(t_101)
                    line_pot_101.set_ydata(pot_101)

                    line_ax_101.set_xdata(t_101)
                    line_ax_101.set_ydata(ax_101_list)

                    line_ay_101.set_xdata(t_101)
                    line_ay_101.set_ydata(ay_101_list)

                    line_az_101.set_xdata(t_101)
                    line_az_101.set_ydata(az_101_list)

                    # relim/autoscale
                    ax101_pot.relim()
                    ax101_pot.autoscale_view()
                    ax101_3axes.relim()
                    ax101_3axes.autoscale_view()

                # -- ID=0x201
                elif msg.arbitration_id == can_id_201:
                    data_list = parse_sensor_data(msg.data.hex())
                    current_time = time.time() - start_time
                    # data_list: [Pot, Gx, Gy, Gz]
                    t_201.append(current_time)
                    pot_201.append(data_list[0])
                    gx_201_list.append(data_list[1])
                    gy_201_list.append(data_list[2])
                    gz_201_list.append(data_list[3])

                    line_pot_201.set_xdata(t_201)
                    line_pot_201.set_ydata(pot_201)

                    line_gx_201.set_xdata(t_201)
                    line_gx_201.set_ydata(gx_201_list)

                    line_gy_201.set_xdata(t_201)
                    line_gy_201.set_ydata(gy_201_list)

                    line_gz_201.set_xdata(t_201)
                    line_gz_201.set_ydata(gz_201_list)

                    ax201_pot.relim()
                    ax201_pot.autoscale_view()
                    ax201_3axes.relim()
                    ax201_3axes.autoscale_view()

            # 3) Κάνουμε redraw μόνο κάθε PLOT_INTERVAL
            now = time.time()
            if (now - last_plot_time) >= PLOT_INTERVAL:
                fig101.canvas.draw()
                fig201.canvas.draw()
                plt.pause(0.0000001)
                last_plot_time = now

            # 4) Μικρό delay για να μην τρέχει το loop στο 100% CPU
            time.sleep(0.000001)

    except KeyboardInterrupt:
        print("\nUser interrupted. Stopping live plot...")

    finally:
        bus.shutdown()
        plt.ioff()
        plt.show()
# --------------------------------------------------------------
# 3) Επιλογή main: Είτε καλείς receive_filtered_can_messages(),
#    είτε καλείς live_plot_can_fast().
# --------------------------------------------------------------

# ---------------------------------------------------------------
# ΝΕΑ ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΑΠΟΘΗΚΕΥΣΗ CAN FRAMES ΣΕ CSV
# ---------------------------------------------------------------
def log_can_frames_to_csv(csv_filename, channel="can0", bitrate=500000):
    """
    Συνάρτηση που ανοίγει το 'csv_filename' και καταγράφει ΟΛΑ τα CAN μηνύματα
    (ή μπορείς να φιλτράρεις συγκεκριμένα IDs) με timestamp, arbitration_id, DLC, data (hex), κλπ.
    Χρησιμοποιεί draining λογική για να μην μπλοκάρει το loop.
    """

    # Ρύθμιση interface
    subprocess.run(['sudo', 'ip', 'link', 'set', channel, 'down'])
    subprocess.run(['sudo', 'ip', 'link', 'set', channel, 'up', 'type', 'can', 'bitrate', str(bitrate)])
    bus = can.interface.Bus(channel=channel, bustype="socketcan")

    # Άνοιγμα CSV για εγγραφή
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        # Επικεφαλίδες στηλών
        writer.writerow(["Timestamp", "ID", "Sensor1", "Sensor2", "Sensor3", "Sensor4"])

        print(f"Logging CAN frames to {csv_filename} (channel={channel}, bitrate={bitrate})")
        print("Πατήστε Ctrl+C για διακοπή.\n")
        start_time = time.time()

        try:
            while True:
                # Διαβάζουμε ΟΛΑ τα διαθέσιμα μηνύματα
                new_msgs = []
                while True:
                    msg = bus.recv(timeout=0.0)
                    if msg is None:
                        break
                    new_msgs.append(msg)

                # Αποθήκευση στο CSV
                for msg in new_msgs:
                    current_time = time.time()
                    real_time_stamp = time.strftime('%H:%M:%S') + f".{int(time.time() * 1000) % 1000:03d}"  # HH:MM:SS.mmm
                    arbitration_id = msg.arbitration_id
                    #data_hex = msg.data.hex()

                    #sensor_data = []
                    #for i in range(0, len(data_hex), 4):
                    # Παίρνουμε κάθε ζεύγος bytes για κάθε αισθητήρα (2 bytes ανά αισθητήρα)
                        #sensor_bytes = bytes.fromhex(data_hex[i:i+4])
                        #sensor_value = convert_sensor_data(sensor_bytes)
                        #sensor_data.append(sensor_value)
                    
                    sensor_data = unified_decode(arbitration_id,msg.data)

                    # Αν θες να φιλτράρεις μόνο 0x101 & 0x201, π.χ.:
                    # if arbitration_id not in [0x101, 0x201]:
                    #    continue
                    
                    sens_values = []
                    # Γράψε τη γραμμή στο CSV
                    for value in sensor_data.values():
                        sens_values.append(value)
                        
                    writer.writerow([f"{real_time_stamp}", f"0x{arbitration_id:X}", f"{sens_values [0]}", f"{sens_values [1]}", f"{sens_values [2]}", f"{sens_values [3]}"])

                # Μικρός ύπνος για να μην είμαστε στο 100% CPU
                time.sleep(0.0001)

        except KeyboardInterrupt:
            print("\nUser interrupted. CSV logging stopped.")
        finally:
            bus.shutdown()


################################################################################
# 3) ???????? ??? Live Plot
################################################################################
    

if __name__ == "__main__":
    receive_filtered_can_messages()
    #live_plot_can()
    #live_plot_can_pyqtgraph()
    # log_can_frames_to_csv("testhmmy.csv")

    #canvas = LiveCANPlot("can0", 500000)
    #canvas.show()
    #app.run()