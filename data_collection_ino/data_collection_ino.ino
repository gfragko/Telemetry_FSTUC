// Define sensor pins (assuming analog sensors for simplicity)
const int sensor1Pin = A0;
const int sensor2Pin = A1;
const int sensor3Pin = A2;

// Buffer to hold sensor readings
char dataPacket[200];  // Large enough to hold all the readings over 1 second
int packetIndex = 0;   // Index to keep track of where to write in the packet

unsigned long lastSendTime = 0;
const unsigned long interval = 1000;  // 1 second

void setup() {
  // Initialize serial communication with Raspberry Pi
  Serial.begin(9600); 

  

  // Initialize sensors (if required)
  pinMode(sensor1Pin, INPUT);
  pinMode(sensor2Pin, INPUT);
  pinMode(sensor3Pin, INPUT);

  // Initialize the packet with an empty string
  memset(dataPacket, 0, sizeof(dataPacket));
}

void loop() {
  // Read sensor data
  int sensor1Data = analogRead(sensor1Pin);
  int sensor2Data = analogRead(sensor2Pin);
  int sensor3Data = analogRead(sensor3Pin);

  // Add the current sensor readings to the data packet
  packetIndex += snprintf(dataPacket + packetIndex, sizeof(dataPacket) - packetIndex, 
                          "%d,%d,%d|", sensor1Data, sensor2Data, sensor3Data);

  // Check if one second has passed
  unsigned long currentTime = millis();
  if (currentTime - lastSendTime >= interval) {
    // Add a newline at the end of the packet to mark its completion
    snprintf(dataPacket + packetIndex, sizeof(dataPacket) - packetIndex, "\n\n");

    // Send the entire packet over Serial to the Raspberry Pi
    Serial.write(dataPacket);

    // Reset the packet for the next second
    memset(dataPacket, 0, sizeof(dataPacket));  // Clear the packet buffer
    packetIndex = 0;  // Reset index

    // Update the last send time
    lastSendTime = currentTime;
  }

  // Optional: Add a small delay to control the sampling rate (e.g., 100ms for 10 readings per second)
  delay(100);
}
