#include <Wire.h>
#include <RTClib.h>

// Create an RTC object
RTC_DS3231 rtc;  // Change to RTC_DS1307 if using the DS1307

// Define your sensor pins
const int sensor1Pin = A0;
const int sensor2Pin = A1;
const int sensor3Pin = A2;
int setup_second;
int start_second;
int start_minute;
int start_hour;
int start_millis = -1;


int millis_handler(){
    int current_millis = millis() % 1000;
    int result;
    if (current_millis < start_millis){
        result = 1000 + (current_millis - start_millis);
    }else{
        result = current_millis - start_millis;
    }

    return result;
}





void get_timestamp(unsigned long current_millis, int timestamp[]){


    unsigned long real_millis = current_millis - start_millis;


    unsigned long milliseconds = real_millis % 1000;
    unsigned int seconds = ((real_millis / 1000) + start_second) % 60; 
    int temp = (((real_millis / 1000) + start_second) / 60);
    int minutes = (temp + start_minute) % 60; 
    int hours = ((minutes/60) + start_hour) % 24;

    timestamp[0] = (int) hours;
    timestamp[1] = (int) minutes;
    timestamp[2] = (int) seconds;
    timestamp[3] = (int) milliseconds;


}

void send_measurements(){
    // DateTime now = rtc.now();

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





    
    Serial.print(timestamp[0]); //Hour
    Serial.print(':');
    Serial.print(timestamp[1]); //Minute
    Serial.print(':');
    Serial.print(timestamp[2]); //Second
    Serial.print('.');
    Serial.print(msString); // Millisecond
    Serial.print(",");  // CSV format
    Serial.print(sensor1Value);
    Serial.print(",");
    Serial.print(sensor2Value);
    Serial.print(",");
    Serial.println(sensor3Value);

    // Delay for a second (or adjust based on your needs)
    delay(10);
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
    DateTime now = rtc.now();
    setup_second=now.second();

}


void loop() {
    DateTime now = rtc.now();
    if(now.second() != setup_second){
        //note start of measurements so we can calculate the correct timestamp
        if(start_millis == -1){ //This runs only once on start up
            start_millis = millis();
            start_second = now.second();
            start_minute = now.minute();
            start_hour = now.hour();
        }

        send_measurements();
        setup_second = -1;// ensures that the current second is always diffrent from setup_second
    }

 




}
