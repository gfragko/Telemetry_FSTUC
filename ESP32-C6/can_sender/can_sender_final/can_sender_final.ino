#include <SPI.h>
#include <mcp_can.h>
#include <Wire.h>
#include <MPU6050.h>

#define CAN0_INT 2                              // Set INT to pin 2
MCP_CAN CAN0(18);                               // Set CS to pin 10

MPU6050 mpu;

#define ID_SENSOR_DATA_101 0x101  // CAN message ID for front left wheel and sensors potentiometer and accelerator
#define ID_SENSOR_DATA_201 0x201  // CAN message ID for front left wheel and sensors gyroscope and hall-effect

//#define ID_SENSOR_DATA 0x102  // CAN message ID for front right wheel and sensors potentiometer and accelerator
//#define ID_SENSOR_DATA 0x202  // CAN message ID for front right wheel and sensors gyroscope and hall-effect

//#define ID_SENSOR_DATA 0x103  // CAN message ID for rear right wheel and sensors potentiometer and accelerator
//#define ID_SENSOR_DATA 0x203  // CAN message ID for rear right wheel and sensors gyroscope and hall-effect

//#define ID_SENSOR_DATA 0x104  // CAN message ID for rear left wheel and sensors potentiometer and accelerator
//#define ID_SENSOR_DATA 0x204  // CAN message ID for rear left wheel and sensors gyroscope and hall-effect

// Sensor pins
const int potentiometerPin = 3;    // Use a valid ADC pin on ESP32 for petensiometer

const int SDA_PIN = 5;    // Use a valid sda pin on ESP32 for MPU6050
const int SCL_PIN = 4;    // Use a valid scl pin on ESP32 for MPU6050

// const int hallEffectPin = 0; // Use a valid pin on ESP32 for Hall Effect sensor

void setup()
{
  Serial.begin(115200);  // CAN is running at 500,000BPS; 115,200BPS is SLOW, not FAST, thus 9600 is crippling.
  
  // Initialize MCP2515 running at 16MHz with a baudrate of 500kb/s and the masks and filters disabled.
  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK) //By default ECU operates at 1MBPS
    Serial.println("MCP2515 Initialized Successfully!");
  else
    Serial.println("Error Initializing MCP2515...");
  
  // Since we do not set NORMAL mode, we are in loopback mode by default.
  CAN0.setMode(MCP_NORMAL);

  pinMode(CAN0_INT, INPUT);                           // Configuring pin for /INT input

  // Initialize I2C communication with custom SDA and SCL pins
  Wire.begin(SDA_PIN, SCL_PIN); // Initialize I2C with custom pins

  // Initialize MPU6050
  mpu.initialize();

  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed!");
    while (1);  // Stop the program if MPU6050 is not connected
  } else {
    Serial.println("MPU6050 initialized successfully.");
  }

}

void sendCanData(int id,int16_t value1,int16_t x,int16_t y,int16_t z){

    // Prepare a CAN data frame (8 bytes total)
    unsigned char data[8] = {0};

    // Split the 16-bit value into high and low bytes
    data[0] = lowByte(value1);  // Low byte
    data[1] = highByte(value1); // High byte

    data[2] = lowByte(x);  // Low byte of x
    data[3] = highByte(x); // High byte of x

    data[4] = lowByte(y);  // Low byte of y
    data[5] = highByte(y); // High byte of y

    data[6] = lowByte(z);  // Low byte of z
    data[7] = highByte(z); // High byte of z

    // Send the data array over CAN (example with 8 bytes)
    if ((id == 101) && (CAN0.sendMsgBuf(ID_SENSOR_DATA_101, 0, 8, data) == CAN_OK)) {
        Serial.println("Message sent successfully_101.");
        
        // Print the CAN frame details
        Serial.print("CAN Frame - ID: 0x");
        Serial.print(ID_SENSOR_DATA_101, HEX);
        Serial.print(", DLC: 3, Data: ");
        for (int i = 0; i < 8; i++) { // Adjusted to only print valid data
            Serial.print("0x");
            Serial.print(data[i], HEX);
            Serial.print(" ");
        }
        Serial.println();
    } else if ((id == 201) && (CAN0.sendMsgBuf(ID_SENSOR_DATA_201, 0, 8, data) == CAN_OK)){
        Serial.println("Message sent successfully_201.");
        
        // Print the CAN frame details
        Serial.print("CAN Frame - ID: 0x");
        Serial.print(ID_SENSOR_DATA_201, HEX);
        Serial.print(", DLC: 3, Data: ");
        for (int i = 0; i < 8; i++) { // Adjusted to only print valid data
            Serial.print("0x");
            Serial.print(data[i], HEX);
            Serial.print(" ");
        }
        Serial.println();
    }else{
        Serial.println("Error sending message.");
    }

}

void readAndSendSensorData() {
    // Read analog sensor values
    int16_t potentiometerValue = analogRead(potentiometerPin);

    int16_t ax, ay, az, gx, gy, gz;

    // Read acceleration and gyroscope data
    mpu.getAcceleration(&ax, &ay, &az);  // Read accelerometer data
    mpu.getRotation(&gx, &gy, &gz);      // Read gyroscope data

    sendCanData(101,potentiometerValue,ax,ay,az);
    sendCanData(201,potentiometerValue,gx,gy,gz); // We must change potetiometer value with hall effect sensor value

}

void loop() {
    readAndSendSensorData(); // Read sensors and send data
    delay(10);              // Increase delay to reduce bus flooding
}