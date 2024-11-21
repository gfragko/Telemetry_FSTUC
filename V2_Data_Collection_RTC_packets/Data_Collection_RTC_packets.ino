#include <Wire.h>
#include <RTClib.h>
#include <Ds1302.h>


// Define RTC pins
#define RSTPIN 7
#define CLK_PIN 6
#define DATA_PIN 5

// Create an RTC object
Ds1302 rtc(RSTPIN, CLK_PIN, DATA_PIN);
// Create an RTC object
// RTC_DS3231 rtc;  // Change to RTC_DS1307 if using the DS1307

// Define your sensor pins
const int sensor1Pin = A0;
const int sensor2Pin = A1;
const int sensor3Pin = A2;
int setup_second;
int start_second;
int start_minute;
int start_hour;
int start_millis = -1;
char dataPacket[200];  // Large enough to hold all the readings over 1 second
int packetIndex = 0;   // Index to keep track of where to write in the packet
int packet_counter = 0;
// unsigned long lastSendTime = 0;
// const unsigned long interval = 1000;  // 1 second



void get_timestamp(unsigned long current_millis, int timestamp[]){


    unsigned long real_millis = current_millis - start_millis;


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
    // DateTime now = rtc.now();
    packet_counter++;

    // Read sensor values
    int sensor1Value = analogRead(sensor1Pin);
    int sensor2Value = analogRead(sensor2Pin);
    int sensor3Value = analogRead(sensor3Pin);
    unsigned long current_millis = millis();

    // Get the current time from the RTC
    // DateTime now = rtc.now();

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
    }

    // 10 measurements per packet
    delay(100);
}



void setup() {
    Serial.begin(9600);
  
    // Initialize the RTC
    if (!rtc.begin()) {
        Serial.println("Couldn't find RTC");
        while (1);
    }
    
    // Check if the RTC is running
    if (rtc.lostPower()) {
        Serial.println("RTC lost power, setting the time!");
        // Uncomment the line below to set the time when needed
        // rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    }
    // DateTime now = rtc.now();
    // start_second = now.second();
    // start_minute = now.minute();
    // start_hour = now.hour();

    // Get the current time
    DS1302::DateTime now = rtc.getDateTime();
    start_second = now.second;
    start_minute = now.minute;
    start_hour = now.hour;

    // Print the time
    Serial.print("Time: ");
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
