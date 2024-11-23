#include "libraries/TFT_eSPI/TFT_eSPI.h"       // TFT library
#include <Wire.h>           // I2C library
#include "libraries/Adafruit_MPU6050/Adafruit_MPU6050.h"
#include <Adafruit_Sensor.h>
#include "libraries/ESP32CAN/ESP32CAN.h"
#include "libraries/CAN_config/CAN_config.h"


// Initialize the TFT and MPU6050
TFT_eSPI tft = TFT_eSPI();
TFT_eSPI tft = TFT_e;
tft.invertDisplay(true);
Adafruit_MPU6050 mpu;
// Orientation variables
float pitch = 0, roll = 0;
float prevPitch = 0, prevRoll = 0; // Store previous values for comparison
float temp = 0, prevTemp = 0;
void setup() { 
    // Initialize Serial, TFT, and MPU6050
    Serial.begin(115200);
    tft.init();
    tft.setRotation(1); // Landscape mode
    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    tft.setTextSize(2);

    if (!mpu.begin()) {
        tft.setCursor(0, 0);
        tft.setTextColor(TFT_RED);
        tft.println("MPU6050 Init Failed!");
        while (1);
    }

    mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
    mpu.setGyroRange(MPU6050_RANGE_250_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

    // Display static labels
    tft.setCursor(10, 10);
    tft.setTextColor(TFT_WHITE);
    tft.println("MPU6050 Data:");
    tft.setCursor(10, 50);
    tft.setTextColor(TFT_YELLOW);
    tft.println("Pitch:");
    tft.setCursor(10, 90);
    tft.setTextColor(TFT_CYAN);
    tft.println("Roll:");
    tft.setCursor(10, 130);
    tft.setTextColor(TFT_GREEN);
    tft.println("Temp:");
}

void loop() {
    // Get sensor data
    sensors_event_t accel, gyro, tempEvent;
    mpu.getEvent(&accel, &gyro, &tempEvent);

    // Calculate pitch and roll from accelerometer data
    pitch = atan2(accel.acceleration.y, accel.acceleration.z) * 180 / PI;
    roll = atan2(-accel.acceleration.x, sqrt(accel.acceleration.y * accel.acceleration.y + accel.acceleration.z * accel.acceleration.z)) * 180 / PI;
    temp = tempEvent.temperature;

    // Update only if values change significantly
    if (abs(pitch - prevPitch) > 0.1) {
        tft.setTextColor(TFT_BLACK); // Overwrite previous value with black
        tft.setCursor(80, 50);
        tft.printf("%.2f   ", prevPitch); // Clear previous value
        tft.setTextColor(TFT_YELLOW);
        tft.setCursor(80, 50);
        tft.printf("%.2f", pitch); // Write new value
        prevPitch = pitch;
    }

    if (abs(roll - prevRoll) > 0.1) {
        tft.setTextColor(TFT_BLACK); // Overwrite previous value with black
        tft.setCursor(80, 90);
        tft.printf("%.2f   ", prevRoll); // Clear previous value
        tft.setTextColor(TFT_CYAN);
        tft.setCursor(80, 90);
        tft.printf("%.2f", roll); // Write new value
        prevRoll = roll;
    }

    if (abs(temp - prevTemp) > 0.1) {
        tft.setTextColor(TFT_BLACK); // Overwrite previous value with black
        tft.setCursor(80, 130);
        tft.printf("%.2f   ", prevTemp); // Clear previous value
        tft.setTextColor(TFT_GREEN);
        tft.setCursor(80, 130);
        tft.printf("%.2f", temp); // Write new value
        prevTemp = temp;
    }

    delay(100); // Adjust update interval
}
