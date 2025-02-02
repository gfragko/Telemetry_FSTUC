#include <SPI.h>

// Default SPI pins for ESP32
void printSPIPins() {
    Serial.println("Default SPI pins for ESP32:");
    Serial.printf("MOSI: GPIO %d\n", MOSI);
    Serial.printf("MISO: GPIO %d\n", MISO);
    Serial.printf("SCK: GPIO %d\n", SCK);
    Serial.printf("SS: GPIO %d\n", SS);
}

void setup() {
    Serial.begin(115200);
    delay(1000);

    // Print default SPI pins
    printSPIPins();
}

void loop() {
    // Nothing to do in the loop
}