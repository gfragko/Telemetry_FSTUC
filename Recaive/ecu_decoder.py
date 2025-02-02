import can
import struct
import sys
import time
import subprocess

# ECU Message IDs όπως δίνονται στον πίνακα
ID_ECU_520 = 0x520  # RPM, Throttle position, MAP, Lambda
ID_ECU_521 = 0x521  # Lambda A, Ignition angle, Ignition cut
ID_ECU_522 = 0x522  # Fuel cut, Vehicle Speed
ID_ECU_524 = 0x524  # Lambda correction A
ID_ECU_530 = 0x530  # Battery voltage, Intake air temp, Coolant temp
ID_ECU_536 = 0x536  # Gear, Oil pressure, Oil temp
ID_ECU_537 = 0x537  # Coolant pressure
ID_ECU_527 = 0x527  # Lambda target
ID_ECU_542 = 0x542  # ECU errors code(s)

def decode_ecu_message(msg):
    """
    Αποκωδικοποιεί το μήνυμα CAN ανάλογα με το CAN ID του.
    Οι τιμές που προκύπτουν μετατρέπονται σύμφωνα με τις κλίμακες που δίνονται,
    και επιστρέφει ένα array (λίστα) με τις τελικές τιμές.
    """
    data = msg.data
    can_id = msg.arbitration_id
    sensor_values = []  # Array με τις τελικές τιμές που θα επιστραφούν

    try:
        if can_id == ID_ECU_520:
            # 0x520: [RPM (offset 0, scale 1), Throttle (offset 2, scale 0.1), 
            #         MAP (offset 4, scale 0.1), Lambda (offset 6, scale 0.001)]
            if len(data) < 8:
                print("Data length error for 0x520")
                return None

            rpm, = struct.unpack_from('<h', data, 0)
            throttle, = struct.unpack_from('<h', data, 2)
            map_val, = struct.unpack_from('<h', data, 4)
            lambda_val, = struct.unpack_from('<h', data, 6)

            sensor_values = [rpm, throttle * 0.1, map_val * 0.1, lambda_val * 0.001]

            print(f"RPM: {rpm}")
            print(f"Throttle Position: {throttle * 0.1:.1f} %")
            print(f"MAP: {map_val * 0.1:.1f} kPa")
            print(f"Lambda: {lambda_val * 0.001:.3f}")

        elif can_id == ID_ECU_521:
            # 0x521: [Lambda A (offset 0, scale 0.001), Ignition angle (offset 4, scale 0.1), 
            #         Ignition cut (offset 6, scale 1)]
            if len(data) < 8:
                print("Data length error for 0x521")
                return None

            lambda_a, = struct.unpack_from('<h', data, 0)
            ignition_angle, = struct.unpack_from('<h', data, 4)
            ignition_cut, = struct.unpack_from('<h', data, 6)

            sensor_values = [lambda_a * 0.001, ignition_angle * 0.1, ignition_cut]

            print(f"Lambda A: {lambda_a * 0.001:.3f}")
            print(f"Ignition Angle: {ignition_angle * 0.1:.1f} BTDC")
            print(f"Ignition Cut: {ignition_cut} %")

        elif can_id == ID_ECU_522:
            # 0x522: [Fuel cut (offset 4, scale 1), Vehicle Speed (offset 6, scale 0.1)]
            if len(data) < 8:
                print("Data length error for 0x522")
                return None

            fuel_cut, = struct.unpack_from('<h', data, 4)
            vehicle_speed, = struct.unpack_from('<h', data, 6)

            sensor_values = [fuel_cut, vehicle_speed * 0.1]

            print(f"Fuel Cut: {fuel_cut} %")
            print(f"Vehicle Speed: {vehicle_speed * 0.1:.1f} km/h")

        elif can_id == ID_ECU_524:
            # 0x524: [Lambda Correction A (offset 2, scale 0.1)]
            if len(data) < 4:
                print("Data length error for 0x524")
                return None

            lambda_corr_a, = struct.unpack_from('<h', data, 2)
            sensor_values = [lambda_corr_a * 0.1]

            print(f"Lambda Correction A: {lambda_corr_a * 0.1:.1f} %")

        elif can_id == ID_ECU_530:
            # 0x530: [Battery voltage (offset 0, scale 0.01), Intake air temp (offset 4, scale 0.1), 
            #         Coolant temp (offset 6, scale 0.1)]
            if len(data) < 8:
                print("Data length error for 0x530")
                return None

            batt_voltage, = struct.unpack_from('<h', data, 0)
            intake_air_temp, = struct.unpack_from('<h', data, 4)
            coolant_temp, = struct.unpack_from('<h', data, 6)

            sensor_values = [batt_voltage * 0.01, intake_air_temp * 0.1, coolant_temp * 0.1]

            print(f"Battery Voltage: {batt_voltage * 0.01:.2f} V")
            print(f"Intake Air Temp: {intake_air_temp * 0.1:.1f} °C")
            print(f"Coolant Temp: {coolant_temp * 0.1:.1f} °C")

        elif can_id == ID_ECU_536:
            # 0x536: [Gear (offset 0, scale 1), Oil pressure (offset 4, scale 0.1), Oil temp (offset 6, scale 0.1)]
            if len(data) < 8:
                print("Data length error for 0x536")
                return None

            gear, = struct.unpack_from('<h', data, 0)
            oil_pressure, = struct.unpack_from('<h', data, 4)
            oil_temp, = struct.unpack_from('<h', data, 6)

            sensor_values = [gear, oil_pressure * 0.1, oil_temp * 0.1]

            print(f"Gear: {gear}")
            print(f"Oil Pressure: {oil_pressure * 0.1:.1f} kPa")
            print(f"Oil Temp: {oil_temp * 0.1:.1f} °C")

        elif can_id == ID_ECU_537:
            # 0x537: [Coolant pressure (offset 4, scale 0.1)]
            if len(data) < 6:
                print("Data length error for 0x537")
                return None

            coolant_pressure, = struct.unpack_from('<h', data, 4)
            sensor_values = [coolant_pressure * 0.1]

            print(f"Coolant Pressure: {coolant_pressure * 0.1:.1f} kPa")

        elif can_id == ID_ECU_527:
            # 0x527: [Lambda target (offset 6, scale 0.001)]
            if len(data) < 8:
                print("Data length error for 0x527")
                return None

            lambda_target, = struct.unpack_from('<h', data, 6)
            sensor_values = [lambda_target * 0.001]

            print(f"Lambda Target: {lambda_target * 0.001:.3f}")

        elif can_id == ID_ECU_542:
            # 0x542: [ECU errors code(s) (offset 4, scale 0.1)]
            if len(data) < 6:
                print("Data length error for 0x542")
                return None

            ecu_errors, = struct.unpack_from('<h', data, 4)
            sensor_values = [ecu_errors]

            print(f"ECU Errors: {ecu_errors}")

        else:
            # Αν το CAN ID δεν είναι αναγνωρισμένο, επιστρέφουμε το raw array
            sensor_values = list(data)

            raw_data = ' '.join(f'0x{byte:02X}' for byte in data)
            print(f"Unknown CAN ID. Raw data: {raw_data}")

        return sensor_values

    except struct.error as e:
        print(f"Error decoding message: {e}")
        return None

def main(channel="can0"):
    # Διαμόρφωση του CAN bus
    # Προσαρμόστε το bustype, το channel, και το bitrate ανάλογα με το hardware σας.
    try:
        subprocess.run(['sudo', 'ip', 'link', 'set', 'can0', 'down'])
        subprocess.run(['sudo', 'ip', 'link', 'set', 'can0', 'up', 'type', 'can', 'bitrate', '500000'])
        bus = can.interface.Bus(channel=channel, bustype="socketcan")
        #bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000)
    except Exception as e:
        print("Error initializing CAN interface:", e)
        sys.exit(1)

    print("Listening for ECU CAN messages...")

    # Συνεχής λήψη μηνυμάτων
    while True:
        try:
            # Blocking call με timeout (σε δευτερόλεπτα)
            msg = bus.recv(timeout=1.0)
            if msg is not None:
                sensor_array = decode_ecu_message(msg)
                if sensor_array is not None:
                    print(f"Decoded values for CAN ID 0x{msg.arbitration_id:X}: {sensor_array}")
            # Αν δεν ληφθεί μήνυμα εντός του timeout, κάνουμε pass
            else:
                pass

        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting...")
            break
        except Exception as e:
            print("Error receiving message:", e)
            time.sleep(0.1)

if __name__ == "__main__":
    main()
