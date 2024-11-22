#include <stdio.h>
#include <ThreeWire.h>  
#include <RtcDS1302.h>

ThreeWire myWire(4,5,2); // IO, SCLK, CE
RtcDS1302<ThreeWire> Rtc(myWire);
// CONNECTIONS:
// DS1302 CLK/SCLK --> 5
// DS1302 DAT/IO --> 4
// DS1302 RST/CE --> 2
// DS1302 VCC --> 3.3v - 5v
// DS1302 GND --> GND


// Define your sensor pins
const int sensor1Pin = A0;
const int sensor2Pin = A1;
const int sensor3Pin = A2;
int start_second;
int start_minute;
int start_hour;
char dataPacket[500];  // Large enough to hold all the readings over 1 second
int packetIndex = 0;   // Index to keep track of where to write in the packet
int packet_counter = 0;



void get_timestamp(unsigned long current_millis, int timestamp[]){
    unsigned long real_millis = current_millis;

    unsigned long milliseconds = real_millis % 1000;
    unsigned int seconds = ((real_millis / 1000) + start_second) % 60; 
    int temp = (((real_millis / 1000) + start_second) / 60);
    int minutes = (temp + start_minute) % 60; 
    int temp_2 = minutes/60 ;
    int hours = (temp_2 + start_hour) % 24;

    timestamp[0] = (int) hours;
    timestamp[1] = (int) minutes;
    timestamp[2] = (int) seconds;
    timestamp[3] = (int) milliseconds;
}

void send_measurements(){
    packet_counter++;

    // Read sensor values
    int sensor1Value = analogRead(sensor1Pin);
    int sensor2Value = analogRead(sensor2Pin);
    int sensor3Value = analogRead(sensor3Pin);
    unsigned long current_millis = millis();


    int timestamp[4];

    get_timestamp(current_millis, timestamp);

    char msString[4]; // Buffer to hold the formatted string

    sprintf(msString, "%03d", timestamp[3]); // Format ms with leading zeros if needed


    
    packetIndex += snprintf(dataPacket + packetIndex, sizeof(dataPacket) - packetIndex, 
                          "%d:%d:%d.%03d,%d,%d,%d|", timestamp[0], timestamp[1], timestamp[2], timestamp[3], sensor1Value, sensor2Value, sensor3Value);

    
    if (packet_counter == 10) {
        // Add a newline at the end of the packet to mark its completion
        snprintf(dataPacket + packetIndex, sizeof(dataPacket) - packetIndex, "\n\n");

        // Send the entire packet over Serial to the Raspberry Pi
        Serial.write(dataPacket);

        // Reset the packet for the next second
        memset(dataPacket, 0, sizeof(dataPacket));  // Clear the packet buffer
        packetIndex = 0;  // Reset index

        // Update the counter
        packet_counter = 0;
        return;
    }

    // 10 measurements per packet
    delay(100);
    return;
}



void setup() {
    Serial.begin(9600);
    

    RtcDateTime now = Rtc.GetDateTime();
    
    
    start_second = now.Second();
    start_minute = now.Minute();
    start_hour = now.Hour();
    Serial.print("Set up time:");
    Serial.print(start_hour);
    Serial.print(":");
    Serial.print(start_minute);
    Serial.print(":");
    Serial.println(start_second);


    // Initialize the packet with an empty string
    memset(dataPacket, 0, sizeof(dataPacket));

}


void loop() {
  send_measurements();
}
