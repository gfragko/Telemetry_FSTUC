#include <mcp_can.h>

define CAN0_INT 2                             // Set INT to pin 2   for arduino or 21 for esp32
MCP_CAN CAN0(10);                               // Set CS to pin 10 for arduino or 5 for esp32

#define ID_SENSOR_DATA 0x101  // CAN message ID for sensor data

void setup() {

    Serial.begin(115200);  // CAN is running at 500,000BPS; 115,200BPS is SLOW, not FAST, thus 9600 is crippling.
    
    // Initialize MCP2515 running at 16MHz with a baudrate of 500kb/s and the masks and filters disabled.
    if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ) == CAN_OK)
        Serial.println("MCP2515 Initialized Successfully!");
    else
        Serial.println("Error Initializing MCP2515...");
    
    // Since we do not set NORMAL mode, we are in loopback mode by default.
    CAN0.setMode(MCP_NORMAL);

    pinMode(CAN0_INT, INPUT);                           // Configuring pin for /INT input

    // Configure mask and filter to listen only to TARGET_CAN_ID
    CAN.init_Mask(0, 1, 0x7FF); // Mask 0: Full 11-bit ID match
    CAN.init_Filt(0, 1, TARGET_CAN_ID); // Filter 0: Match TARGET_CAN_ID

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