#include <stdio.h>
#include <ThreeWire.h>
#include <mcp2515.h>

#define CAN_CS_PIN 10 // CAN controller chip select pin
#define TARGET_CAN_ID 0x101 // Target CAN message ID

// MCP2515 CAN configuration
struct can_frame canMsg;      // CAN frame structure
MCP2515 mcp2515(CAN_CS_PIN);  // MCP2515 instance on CS pin 10

void setup() {
    Serial.begin(115200);
    Serial.println("CAN Receiver - ESP32-Arduino with MCP2515");
    
    // Initialize SPI and MCP2515
    SPI.begin();
    mcp2515.reset();

    // Set MCP2515 to Normal mode and configure speed
    mcp2515.setBitrate(CAN_125KBPS);

    mcp2515.setFilterMask(MCP2515::MASK0, true, 0x7FF); // Full match mask for 11-bit IDs
    mcp2515.setFilter(MCP2515::RXF0, true, TARGET_CAN_ID); // Set filter for the specific ID


    mcp2515.setNormalMode();

    Serial.print("MCP2515 initialized. Listening for CAN ID: 0x");
    Serial.println(TARGET_CAN_ID, HEX);
}

void loop() {
    // Check for incoming CAN messages
    if (mcp2515.readMessage(&canMsg) == MCP2515::ERROR_OK && canMsg.can_id == TARGET_CAN_ID) {  
        Serial.print("Received CAN message with ID: 0x");
        Serial.println(canMsg.can_id, HEX);

        Serial.print("Data: ");
        for (int i = 0; i < canMsg.can_dlc; i++) {
            Serial.print(canMsg.data[i], DEC); // Print data as decimal
            Serial.print(" ");
        }
        Serial.println();
        
    }
}
