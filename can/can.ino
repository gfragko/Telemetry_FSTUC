#include <ThreeWire.h>         // Library for 3-wire (software SPI)
#include <RtcDS1302.h>         // Library for DS1302 RTC
#include <SPI.h>               // SPI library for CAN bus
#include <mcp_can.h>           // MCP2515 CAN controller library

// Pin definitions
#define RSTPIN 2    // RTC reset pin
#define DATPIN 3    // RTC data pin
#define CLKPIN 4    // RTC clock pin
#define CAN_CS_PIN 10 // CAN controller chip select pin

// Initialize 3-Wire and RTC objects
ThreeWire myWire(DATPIN, CLKPIN, RSTPIN);  // IO, SCLK, CE
RtcDS1302<ThreeWire> rtc(myWire);

// Initialize MCP2515 CAN controller
MCP_CAN CAN0(CAN_CS_PIN);

// Sensor pins
const int sensor1Pin = A0;
const int sensor2Pin = A1;
const int sensor3Pin = A2;

// CAN message IDs
const uint16_t ID_TIMESTAMP = 0x100;
const uint16_t ID_SENSOR_DATA = 0x101;

// Data buffers for CAN frames
unsigned char timestampData[8];
unsigned char sensorData[8];

void setup() {
    Serial.begin(9600);

    // Initialize RTC
    rtc.Begin();
    RtcDateTime compiled = RtcDateTime(__DATE__, __TIME__);
    if (!rtc.IsDateTimeValid()) {
        Serial.println("RTC lost power, setting to compiled time!");
        rtc.SetDateTime(compiled);
    }

    // Initialize CAN bus
    if (CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK) {
        Serial.println("CAN bus initialized successfully!");
    } else {
        Serial.println("Error initializing CAN bus.");
        while (1); // Halt if CAN initialization fails
    }
    CAN0.setMode(MCP_NORMAL);
}

void loop() {
    // Get current timestamp from RTC
    RtcDateTime now = rtc.GetDateTime();

    // Read sensor values
    int sensor1Value = analogRead(sensor1Pin);
    int sensor2Value = analogRead(sensor2Pin);
    int sensor3Value = analogRead(sensor3Pin);

    // Format and send the timestamp
    formatTimestampData(now);
    sendCanMessage(ID_TIMESTAMP, timestampData);

    // Format and send the sensor data
    formatSensorData(sensor1Value, sensor2Value, sensor3Value);
    sendCanMessage(ID_SENSOR_DATA, sensorData);

    delay(1000); // Wait 1 second before next transmission
}

// Function to format timestamp data into CAN frame
void formatTimestampData(const RtcDateTime& dt) {
    timestampData[0] = (dt.Year() - 2000); // Years since 2000
    timestampData[1] = dt.Month();
    timestampData[2] = dt.Day();
    timestampData[3] = dt.Hour();
    timestampData[4] = dt.Minute();
    timestampData[5] = dt.Second();
    //timestampData[6] = 0; // Unused bytes
    //timestampData[7] = 0;
}

// Function to format sensor data into CAN frame
void formatSensorData(int sensor1, int sensor2, int sensor3) {
    sensorData[0] = map(sensor1, 0, 1023, 0, 255); // Scale to 8-bit
    sensorData[1] = map(sensor2, 0, 1023, 0, 255);
    sensorData[2] = map(sensor3, 0, 1023, 0, 255);
    sensorData[3] = 0; // Placeholder for additional sensors
    sensorData[4] = 0; // Unused
    sensorData[5] = 0;
    sensorData[6] = 0;
    sensorData[7] = 0;
}

// Function to send CAN messages
void sendCanMessage(uint16_t id, unsigned char* data) {
    if (CAN0.sendMsgBuf(id, 0, 8, data) == CAN_OK) {
        Serial.print("Data sent via CAN bus with ID: 0x");
        Serial.println(id, HEX);
    } else {
        Serial.print("Error sending CAN data with ID: 0x");
        Serial.println(id, HEX);
    }
}
