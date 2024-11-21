#include <Ds1302.h>


// Define RTC pins
#define RSTPIN 7
#define CLK_PIN 6
#define DATA_PIN 5

// Create an RTC object
Ds1302 rtc(RSTPIN, CLK_PIN, DATA_PIN);

void setup() {
    Serial.begin(9600);

    // Initialize RTC
    rtc.begin();

    // Uncomment to set the time (only needed once)
    // rtc.setDateTime(__DATE, __TIME);

    Serial.println("RTC Initialized");
}

void loop() {
    // Get the current time
    DS1302::DateTime now = rtc.getDateTime();

    // Print the time
    Serial.print("Time: ");
    Serial.print(now.hour);
    Serial.print(":");
    Serial.print(now.minute);
    Serial.print(":");
    Serial.println(now.second);

    // Delay for 1 second
    delay(1000);
}
