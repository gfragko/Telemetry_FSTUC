#include <SPI.h>
#include <mcp_can.h>

#define CAN0_INT 2                             // Set INT to pin 2
MCP_CAN CAN0(10);                               // Set CS to pin 10

#define ID_SENSOR_DATA 0x101  // CAN message ID for sensor data

// Sensor pins
const int sensor1Pin = 2;    // Use a valid ADC pin on ESP32

void setup()
{
  Serial.begin(115200);  // CAN is running at 500,000BPS; 115,200BPS is SLOW, not FAST, thus 9600 is crippling.
  
  // Initialize MCP2515 running at 16MHz with a baudrate of 500kb/s and the masks and filters disabled.
  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK)
    Serial.println("MCP2515 Initialized Successfully!");
  else
    Serial.println("Error Initializing MCP2515...");
  
  // Since we do not set NORMAL mode, we are in loopback mode by default.
  CAN0.setMode(MCP_NORMAL);

  pinMode(CAN0_INT, INPUT);                           // Configuring pin for /INT input
  
}

void readAndSendSensorData() {
    // Read analog sensor values
    int sensor1Value = analogRead(sensor1Pin);
    int sensor2Value = 20; // Placeholder for additional sensors
    int sensor3Value = 20; // Placeholder for additional sensors

    // Map sensor values to 8-bit range (0-255)
    unsigned char data[8] = {0};
    data[0] = (char)map(sensor1Value, 0, 1023, 0, 255);
    data[1] = (char)map(sensor2Value, 0, 1023, 0, 255);
    data[2] = (char)map(sensor3Value, 0, 1023, 0, 255);

    // Print the CAN frame details
    Serial.print("CAN Frame - ID: 0x");
    Serial.print(ID_SENSOR_DATA, HEX);
    Serial.print(", DLC: 3, Data: ");
    for (int i = 0; i < 3; i++) { // Adjusted to only print valid data
        Serial.print("0x");
        Serial.print(data[i], HEX);
        Serial.print(" ");
    }
    Serial.println();

    // Send CAN message
    byte sendStatus = CAN0.sendMsgBuf(ID_SENSOR_DATA, 0, 3, data);
    if (sendStatus == CAN_OK) {
        Serial.println("Data sent successfully.");
    } else {
        Serial.println("Error sending data.");
    }
}

void loop() {
    readAndSendSensorData(); // Read sensors and send data
    // delay(1);              // Increase delay to reduce bus flooding
}
