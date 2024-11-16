# Telemetry System for FSTUC
Scripts to extract sensor data for telemetry using an arduino and a rasberry pi.
The arduino gets as input the measurements from the sensors, formats them and passes them to the rasbeery pi.
Τhe rasberry pi logs the data in an sd card and sends the data to a remote location using RF.

### <ins>TODO:</ins>
+ Fix arduino code for correct usage of RTC
+ Transform arduino output for usage of CAN bus
+ Implement sending data to remote pc
+ Create GUI for live data

