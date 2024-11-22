# Telemetry System for FSTUC
Scripts to extract sensor data for telemetry using an arduino and a Raspberry Pi.
The arduino gets as input the measurements from the sensors, formats them and passes them to the Raspberry Pi.
Τhe Raspberry Pi logs the data in a usb and sends the data to a remote location using RF.

### <ins>TODO:</ins>
+ ~~Fix arduino code for correct usage of RTC~~
+ Transform arduino output for usage of CAN bus
+ Implement sending data to remote pc
+ Create GUI for live data
+ Raspberry Pi sever for live data (???)

### <ins>Notes:</ins>
+ **V2_Data_Collection_RTC_packets:** It takes 170ms to send the packet through serial, hence the extra 70ms delay when sending the packet. This does not affect the timestamp accuracy.
+ **File Structure:** New file structure for a cleaner repo. 