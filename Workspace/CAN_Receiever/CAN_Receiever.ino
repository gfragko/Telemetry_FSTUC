#include <mcp_can.h>

#define CAN0_INT 2   
#define CAN_CS_PIN 10        // Chip Select pin for MCP2515
#define TARGET_CAN_ID 0x101   // Target CAN ID to listen for

MCP_CAN CAN0(CAN_CS_PIN);      // Initialize MCP_CAN object

void setup() {
  Serial.begin(115200);
  
  // Initialize MCP2515 running at 16MHz with a baudrate of 500kb/s and the masks and filters disabled.
  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK)
    Serial.println("MCP2515 Initialized Successfully!");
  else
    Serial.println("Error Initializing MCP2515...");
  
  CAN0.setMode(MCP_NORMAL);                     // Set operation mode to normal so the MCP2515 sends acks to received data.

  pinMode(CAN0_INT, INPUT);                            // Configuring pin for /INT input
  
  // Serial.println("MCP2515 Library Receive Example...");
  // // Configure mask and filter to listen only to TARGET_CAN_ID
  // CAN0.init_Mask(0, 1, 0x7FF); // Mask 0: Full 11-bit ID match
  // CAN0.init_Filt(0, 1, TARGET_CAN_ID); // Filter 0: Match TARGET_CAN_ID

  // Serial.print("Listening for CAN ID: 0x");
  // Serial.println(TARGET_CAN_ID, HEX);
}

void loop() {
  // Serial.println("bam");
// Check if data is available
    if (CAN0.checkReceive() == CAN_MSGAVAIL) {//This code checks whether a new CAN message is available in the receive buffer of the MCP2515 CAN controller.
        long unsigned int rxId;
        unsigned char len = 0;
        unsigned char buf[8];

        // Read the message
        if (CAN0.readMsgBuf(&rxId, &len, buf) == CAN_OK) {
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
        Serial.println("Message found");
        delay(2000);
    }
}