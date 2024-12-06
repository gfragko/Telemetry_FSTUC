#include <stdio.h>
#include <ThreeWire.h> 
#include <mcp2515.h>

#define ID_SENSOR_DATA 0x101 // CAN message ID for sensor data
#define CAN_CS_PIN 10 // CAN controller chip select pin

// MCP2515 CAN configuration
struct can_frame canMsg;      // CAN frame structure
MCP2515 mcp2515(CAN_CS_PIN);  // MCP2515 instance on CS pin 10

// Sensor pins
const int sensor1Pin = A0;
const int sensor2Pin = A1;
const int sensor3Pin = A2;

// Function to read sensor data and send it via CAN
void readAndSendSensorData() {
    // Read analog sensor values
    int sensor1Value = analogRead(sensor1Pin);
    int sensor2Value = analogRead(sensor2Pin);
    int sensor3Value = analogRead(sensor3Pin);

    // Map sensor values to 8-bit range (0-255)
    unsigned char mappedValues[8] = {0};
    mappedValues[0] = map(sensor1Value, 0, 1023, 0, 255);
    mappedValues[1] = map(sensor2Value, 0, 1023, 0, 255);
    mappedValues[2] = map(sensor3Value, 0, 1023, 0, 255);

    // Send CAN message
    sendCanMessage(0x101, mappedValues);
}

// Function to send a CAN message
void sendCanMessage(uint16_t id, unsigned char* data) {
    canMsg.can_id = id;       // Set the message ID
    canMsg.can_dlc = 8;       // Set data length (8 bytes)

    // Copy the data into the CAN frame
    for (int i = 0; i < 8; i++) {
        canMsg.data[i] = data[i];
    }

    // Transmit the CAN frame
    if (mcp2515.sendMessage(&canMsg) == MCP2515::ERROR_OK) {
        Serial.print("Data sent via CAN bus with ID: 0x");
        Serial.println(id, HEX);
    } else {
        Serial.print("Error sending CAN data with ID: 0x");
        Serial.println(id, HEX);
    }
}

// Map function to scale values
int map(int x, int in_min, int in_max, int out_min, int out_max) {
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void setup() {
    Serial.begin(115200);
    Serial.println("Basic Demo - ESP32-Arduino-CAN with MCP2515");
    
    // Initialize SPI and MCP2515
    SPI.begin();
    mcp2515.reset();

    // Set MCP2515 to Normal mode and configure speed
    mcp2515.setBitrate(CAN_125KBPS);
    mcp2515.setNormalMode();

    Serial.println("MCP2515 initialized successfully.");
}

void loop() {
    readAndSendSensorData(); // Read sensors and send data
    delay(100);              // Add a small delay to avoid overwhelming the CAN bus
}

