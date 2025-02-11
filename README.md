# Telemetry System for FSTUC
Scripts to extract sensor data for telemetry using an arduino and a Raspberry Pi.
The arduino gets as input the measurements from the sensors, formats them and passes them to the Raspberry Pi.
Τhe Raspberry Pi logs the data in a usb and sends the data to a remote location using RF.

### <ins>TODO:</ins>
+ ~~Fix arduino code for correct usage of RTC~~
+ ~~Transform arduino output for usage of CAN bus~~
+ ~~Send and receive can frames with mcp2515~~
+ ~~Save can messages on ECU~~
+ ~~Set up slaves to master to raspberry pi architecture~~ 
+ ~~Save data locally on raspberry pi via usb~~
+ Denoiser for sensor values
+ Mapping Data for cleaner y-axis
+ Pyqtgraph testing for csv plotting
+ X-Y-Z axis plotting for mpu data 
+ Rounding - Sampling timestamps to decrease x-axis noise
+ Setting up a rasberrry buttin to start telemetry logging
+ Send data through RF
+ Create GUI for live data
+ Raspberry Pi sever for live data (???)

### <ins>Notes:</ins>
+ Use Find_SPI.ino script to figure out the pins to be used on the esp32 board
+ Use gpio 2 (on eps 32) for interrupt on mcp2515
