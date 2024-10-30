#include <Wire.h>
#include <RTClib.h>

// Create an RTC object
RTC_DS3231 rtc;  // Change to RTC_DS1307 if using the DS1307

// Define your sensor pins
const int sensor1Pin = A0;
const int sensor2Pin = A1;
const int sensor3Pin = A2;
int start_second;
int start_millis = -1;
int check_millis = -1;

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
   start_second=now.second();

}

int millis_handler(){
    current_millis = millis() % 1000;
    int result;
    if (current_millis < start_millis){
        result = 1000 + (current_millis - start_millis);
    }else{
        result = current_millis - start_millis;
    }

    return result;
}


void send_measurements(){

    // Read sensor values
    int sensor1Value = analogRead(sensor1Pin);
    int sensor2Value = analogRead(sensor2Pin);
    int sensor3Value = analogRead(sensor3Pin);

    // Get the current time from the RTC
    DateTime now = rtc.now();
    
    // Print the timestamp and sensor values
    Serial.print(now.year(), DEC);
    Serial.print('/');
    Serial.print(now.month(), DEC);
    Serial.print('/');
    Serial.print(now.day(), DEC);
    Serial.print(" ");
    Serial.print(now.hour(), DEC);
    Serial.print(':');
    Serial.print(now.minute(), DEC);
    Serial.print(':');
    Serial.print(now.second(), DEC);
    Serial.print('.');
    int milliseconds = millis_handler();
    Serial.print(milliseconds);  // Milliseconds
    Serial.print(",");  // CSV format
    Serial.print(sensor1Value);
    Serial.print(",");
    Serial.print(sensor2Value);
    Serial.print(",");
    Serial.println(sensor3Value);

    // Delay for a second (or adjust based on your needs)
    delay(1000);
}


void loop() {
    
 if(now.second() != start_second){
  start_second = -1;
  if(start_millis == -1){
    start_millis = millis();
  }

  send_measurements();


  //break loop()
 }

 




}
