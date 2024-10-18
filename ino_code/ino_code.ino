// Pin assignments for sensors
const int potPin1 = A0;
const int potPin2 = A1;
const int tempSensorPin = A2;

void setup() {
  // Start serial communication at 9600 baud rate
  Serial.begin(9600);
}

void loop() {
  // Read values from sensors
  int potValue1 = analogRead(potPin1);  // Potentiometer 1
  int potValue2 = analogRead(potPin2);  // Potentiometer 2
  int tempValue = analogRead(tempSensorPin);  // Temperature sensor

  // Send the sensor values as a comma-separated string
  Serial.print(potValue1);
  Serial.print(",");
  Serial.print(potValue2);
  Serial.print(",");
  Serial.println(tempValue);

  // Delay to match Raspberry Pi logging interval
  delay(50);  // Adjust delay as needed
}
