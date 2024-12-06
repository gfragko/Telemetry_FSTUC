#include "libraries/ESP32-Arduino-CAN-master/src/ESP32CAN.h"
#include "libraries/mcp_can/mcp_can.h"


#define CAN_CS_PIN 5        // Chip Select pin for MCP2515
#define TARGET_CAN_ID 0x101   // Target CAN ID to listen for

MCP_CAN CAN(CAN_CS_PIN);      // Initialize MCP_CAN object

void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("CAN Receiver - Listening to Specific ID");

    // Initialize MCP2515
    if (CAN.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK) {
        Serial.println("MCP2515 Initialized Successfully!");
    } else {
        Serial.println("Error Initializing MCP2515...");
        while (1);
    }

    // Set MCP2515 to Normal Mode
    CAN.setMode(MCP_NORMAL);

    // Configure mask and filter to listen only to TARGET_CAN_ID
    CAN.init_Mask(0, 1, 0x7FF); // Mask 0: Full 11-bit ID match
    CAN.init_Filt(0, 1, TARGET_CAN_ID); // Filter 0: Match TARGET_CAN_ID

    Serial.print("Listening for CAN ID: 0x");
    Serial.println(TARGET_CAN_ID, HEX);
}

void loop() {
// Check if data is available
    if (CAN.checkReceive() == CAN_MSGAVAIL) {//This code checks whether a new CAN message is available in the receive buffer of the MCP2515 CAN controller.
        long unsigned int rxId;
        unsigned char len = 0;
        unsigned char buf[8];

        // Read the message
        if (CAN.readMsgBuf(&rxId, &len, buf) == CAN_OK) {
            // Check if the ID matches the target ID
            if (rxId == TARGET_CAN_ID) {
                Serial.print("Received CAN Message with ID: 0x");
                Serial.println(rxId, HEX);

                Serial.print("Data: ");
                for (int i = 0; i < len; i++) {
                    Serial.print(buf[i], DEC);
                    Serial.print(" ");
                }
                Serial.println();
            }
        }
    }
}