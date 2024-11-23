#include <stdio.h>
#include <ThreeWire.h>  
#include "libraries/ESP32CAN/ESP32CAN.h"
#include "libraries/CAN_config/CAN_config.h"
#include "libraries/Rtc_by_Makuna/src/RtcDS1302.h"

// CAN configuration
#define CAN_CS_PIN 10 // CAN controller chip select pin
#define ID_SENSOR_DATA 0x101 // CAN message ID for sensor data

// Sensor pins
const int sensor1Pin = A0;
const int sensor2Pin = A1;
const int sensor3Pin = A2;

// Function prototypes
void sendCanMessage(uint16_t id, unsigned char* data);
void readAndSendSensorData();
int map(int x, int in_min, int in_max, int out_min, int out_max);

void setup() {
    Serial.begin(115200);
    Serial.println("Basic Demo - ESP32-Arduino-CAN");

    // Configure CAN parameters
    CAN_cfg.speed = CAN_SPEED_125KBPS;
    CAN_cfg.tx_pin_id = GPIO_NUM_5; // Set appropriate GPIO pins
    CAN_cfg.rx_pin_id = GPIO_NUM_4;
    CAN_cfg.rx_queue = xQueueCreate(10, sizeof(CAN_frame_t)); // CAN RX queue

    // Initialize the CAN module
    if (ESP32Can.CANInit() == ESP_OK) {
        Serial.println("CAN module initialized successfully.");
    } else {
        Serial.println("Error initializing CAN module.");
    }
}

void loop() {
    readAndSendSensorData(); // Read sensors and send data
}

// Function to read sensor data and send it via CAN
void readAndSendSensorData() {
    // Read analog sensor values
    int sensor1Value = analogRead(sensor1Pin);
    int sensor2Value = analogRead(sensor2Pin);
    int sensor3Value = analogRead(sensor3Pin);

    // Map sensor values to 8-bit range (0-255)
    unsigned char mappedValues[8] = {0};
    mappedValues[0] = map(sensor1Value, 0, 1023, 0, 255); // Map to 0-255
    mappedValues[1] = map(sensor2Value, 0, 1023, 0, 255); // Map to 0-255
    mappedValues[2] = map(sensor3Value, 0, 1023, 0, 255); // Map to 0-255

    // Send CAN message
    sendCanMessage(ID_SENSOR_DATA, mappedValues);
}

// Function to send a CAN message
void sendCanMessage(uint16_t id, unsigned char* data) {
    CAN_frame_t tx_frame;

    // Set the message ID
    tx_frame.MsgID = id;

    // Configure the frame type
    tx_frame.FIR.B.FF = CAN_frame_std;  // Use CAN_frame_ext for extended frame if needed
    tx_frame.FIR.B.RTR = CAN_no_RTR;    // Data frame (not a Remote Transmission Request)
    tx_frame.FIR.B.DLC = 8;             // Data length (8 bytes)

    // Copy the data into the frame
    for (int i = 0; i < 8; i++) {
        tx_frame.data.u8[i] = data[i];
    }

    // Send the CAN frame
    if (ESP32Can.CANWriteFrame(&tx_frame) == ESP_OK) {
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
