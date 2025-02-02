#include "DTCManager.h"


const TroubleCode DTCManager::troubleCodes[] PROGMEM  = {
{0x0011, "Camshaft Position 'A' - Timing Over-Advanced or System Performance", "Check camshaft position sensor or timing chain."},
  {0x0171, "System Too Lean (Bank 1)", "Check for vacuum leaks, faulty mass airflow sensor, or clogged fuel injectors."},
  {0x0174, "System Too Lean (Bank 2)", "Check for vacuum leaks, faulty mass airflow sensor, or clogged fuel injectors."},
  {0x0300, "Random/Multiple Cylinder Misfire Detected", "Inspect and replace spark plugs or ignition coils if necessary."},
  {0x0420, "Catalyst System Efficiency Below Threshold (Bank 1)", "Check and possibly replace the catalytic converter."},
  {0x0430, "Catalyst System Efficiency Below Threshold (Bank 2)", "Check and possibly replace the catalytic converter."},
  {0x0442, "Evaporative Emission Control System Leak Detected (small leak)", "Inspect for a loose gas cap, cracked hoses, or a faulty purge valve."},
  {0x0455, "Evaporative Emission Control System Leak Detected (large leak)", "Inspect for a loose gas cap, cracked hoses, or a faulty purge valve."},
  {0x0600, "Serial Communication Link Malfunction", "Check communication links and wiring."},
  {0x0601, "Internal Control Module Memory Check Sum Error", "Check or replace the ECU."},
  {0x0602, "Control Module Programming Error", "Reprogram or replace the ECU."},
  {0x0603, "Internal Control Module Keep Alive Memory (KAM) Error", "Inspect wiring, check battery connections, or replace the ECU."},
  {0x0604, "Internal Control Module Random Access Memory (RAM) Error", "Check or replace the ECU."},
  {0x0605, "Internal Control Module Read Only Memory (ROM) Error", "Check or replace the ECU."},
  {0x0606, "ECM/PCM Processor Fault", "Inspect wiring and connectors, or replace the ECM/PCM."},
  {0x0607, "Control Module Performance", "Check the control module and reprogram or replace if necessary."},
  {0x0608, "Control Module VSS Output 'A' Malfunction", "Inspect and replace the Vehicle Speed Sensor (VSS) or the control module."},
  {0x0609, "Control Module VSS Output 'B' Malfunction", "Inspect and replace the Vehicle Speed Sensor (VSS) or the control module."},
  {0x0620, "Generator Control Circuit Malfunction", "Inspect the generator, battery, and wiring."},
  {0x0621, "Generator Lamp 'L' Control Circuit Malfunction", "Check and repair the generator lamp circuit."},
  {0x0622, "Generator Field 'F' Control Circuit Malfunction", "Inspect and repair the generator field circuit."},
  {0x0650, "Malfunction Indicator Lamp (MIL) Control Circuit Malfunction", "Inspect the MIL circuit and repair any issues."},
  {0x0654, "Engine RPM Output Circuit Malfunction", "Check and repair the engine RPM output circuit."},
  {0x0655, "Engine Hot Lamp Output Control Circuit Malfunction", "Inspect and repair the engine hot lamp circuit."},
  {0x0656, "Fuel Level Output Circuit Malfunction", "Inspect the fuel level sensor and repair the circuit."},
  {0x0791, "Intermediate Shaft Speed Sensor 'A' Circuit", "Inspect and replace the intermediate shaft speed sensor."},
  {0x0792, "Intermediate Shaft Speed Sensor 'A' Circuit Range/Performance", "Check the sensor and wiring, replace if necessary."},
  {0x0971, "Shift Solenoid 'C' Control Circuit Range/Performance", "Inspect the shift solenoid 'C' and repair any issues."},
  {0x1000, "OBD-II Monitor Testing Not Complete", "Complete the drive cycle to finish testing."},
  {0x1001, "Manufacturer Control", "Consult manufacturer guidelines for diagnostics."},
  {0x1100, "Manufacturer Control Fuel Air Metering", "Consult manufacturer guidelines for fuel-air metering diagnostics."},
  {0x2610, "ECM/PCM Internal Engine Off Timer Performance", "Check the ECM/PCM and associated wiring."},
  {0x0401, "Exhaust Gas Recirculation (EGR) Flow Insufficient", "Inspect the EGR valve and passages, clean or replace as necessary."},
  {0x0402, "Exhaust Gas Recirculation (EGR) Flow Excessive", "Inspect the EGR valve and control system, replace if needed."},
  {0x0421, "Warm Up Catalyst Efficiency Below Threshold (Bank 1)", "Inspect and replace the catalytic converter."},
  {0x0431, "Warm Up Catalyst Efficiency Below Threshold (Bank 2)", "Inspect and replace the catalytic converter."},
  {0x0507, "Idle Control System RPM Higher Than Expected", "Inspect and clean the idle air control valve, check for vacuum leaks."},
  {0x0128, "Coolant Thermostat (Coolant Temperature Below Thermostat Regulating Temperature)", "Inspect the thermostat and replace if faulty."},
  {0x0135, "O2 Sensor Heater Circuit Malfunction (Bank 1, Sensor 1)", "Inspect and replace the oxygen sensor or heater circuit."},
  {0x0140, "O2 Sensor Performance (Bank 1, Sensor 1)", "Check and replace the oxygen sensor."},
  {0x0141, "O2 Sensor Heater Circuit Malfunction (Bank 1, Sensor 2)", "Inspect and replace the oxygen sensor or heater circuit."},
  {0x0175, "System Too Rich (Bank 2)", "Check for fuel system issues or a malfunctioning mass airflow sensor."},
  {0x0191, "Fuel Temperature Sensor Range/Performance", "Inspect and replace the fuel temperature sensor if necessary."},
  {0x0192, "Fuel Pressure Sensor Range/Performance", "Inspect and replace the fuel pressure sensor if necessary."},
  {0x0200, "Throttle Position Sensor Range/Performance", "Inspect and replace the throttle position sensor if necessary."},
  {0x0210, "Fuel Injector Circuit Malfunction", "Check the fuel injectors and associated wiring."},
  {0x0230, "Intake Air Temperature Sensor Range/Performance", "Inspect and replace the intake air temperature sensor if necessary."},
  {0x0290, "Turbocharger/Supercharger Boost Sensor Range/Performance", "Inspect and replace the boost sensor or associated components."},
  {0x0340, "Camshaft Position Sensor Range/Performance", "Inspect and replace the camshaft position sensor if necessary."},
  {0x0500, "Idle Air Control Circuit Malfunction", "Inspect and replace the idle air control valve."},
  {0x0700, "Transmission Control System Malfunction", "Check the transmission control system and associated components."},
  {0x0900, "Coolant Temperature Sensor Range/Performance", "Inspect and replace the coolant temperature sensor if necessary."},
  {0x1F00, "Manufacturer Specific", "Consult manufacturer-specific diagnostics."},
  {0x1F01, "Manufacturer Specific", "Consult manufacturer-specific diagnostics."},
  {0x1F02, "Manufacturer Specific", "Consult manufacturer-specific diagnostics."},
  {0x1F03, "Manufacturer Specific", "Consult manufacturer-specific diagnostics."},
  {0x1F04, "Manufacturer Specific", "Consult manufacturer-specific diagnostics."},
  
  // Body (B-codes)
  {0x1000, "Body Control Module (BCM) Malfunction", "Inspect and repair the body control module."},
  {0x1001, "Door Lock Circuit Malfunction", "Check door lock actuators and wiring."},
  {0x1002, "Window Motor Circuit Malfunction", "Inspect window motor and wiring."},
  {0x1003, "Lighting Circuit Malfunction", "Inspect and repair lighting circuits."},
  {0x1004, "Climate Control System Fault", "Check climate control system components."},
  {0x1005, "Seat Position Sensor Fault", "Inspect seat position sensors and wiring."},
  {0x1006, "Airbag System Fault", "Inspect airbag system components and wiring."},
  {0x1007, "Instrument Cluster Malfunction", "Check instrument cluster connections and components."},
  
  // Network (U-codes)
  {0x1000, "CAN Communication Error", "Check CAN network wiring and modules."},
  {0x1001, "LIN Communication Error", "Inspect LIN network wiring and modules."},
  {0x1002, "OBD-II Communication Error", "Check OBD-II connector and communication lines."},
  {0x1003, "Module Communication Error", "Inspect and repair communication lines between modules."},
  {0x1004, "Network Signal Fault", "Check for network signal integrity issues."},
  
  // Chassis (C-codes)
  {0x1000, "Anti-lock Brake System (ABS) Fault", "Inspect ABS components and wiring."},
  {0x1001, "Traction Control System (TCS) Fault", "Check TCS components and wiring."},
  {0x1002, "Electronic Stability Program (ESP) Fault", "Inspect ESP system components."},
  {0x1003, "Suspension System Fault", "Check suspension system components and sensors."},
  {0x1004, "Steering Angle Sensor Fault", "Inspect and calibrate steering angle sensor."},
  {0x1005, "Brake Fluid Level Sensor Fault", "Inspect brake fluid level sensor and wiring."},
  {0x1006, "Parking Brake Fault", "Check parking brake system and sensors."},
  {0x1007, "Vehicle Dynamics Control Fault", "Inspect vehicle dynamics control system components."},
};
const int DTCManager::numTroubleCodes = sizeof(DTCManager::troubleCodes) / sizeof(TroubleCode);

DTCManager::DTCManager() {
    // No specific initialization required
}

bool DTCManager::getTroubleCodeDetails(uint16_t code, String &description, String &fix) {
    for (int i = 0; i < numTroubleCodes; i++) {
        TroubleCode codeEntry;
        memcpy_P(&codeEntry, &troubleCodes[i], sizeof(TroubleCode));

        if (codeEntry.code == code) {
            description = codeEntry.description;
            fix = codeEntry.fix;
            return true; // Code found
        }
    }
    return false; // Code not found
}