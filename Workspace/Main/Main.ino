#include "libraries/ESP32-Arduino-CAN-master/src/ESP32CAN.h"
#include "libraries/ESP32-Arduino-CAN-master/src/CAN_config.h"

CAN_device_t CAN_cfg;               // CAN Config
unsigned long previousMillis = 0;   // will store last time a CAN Message was send
const int interval = 1000;          // interval at which send CAN Messages (milliseconds)
const int rx_queue_size = 10;       // Receive Queue size
const uint32_t target_id = 0x101;

void setup() {
  Serial.begin(115200);
  Serial.println("Basic Demo - ESP32-Arduino-CAN");
  CAN_cfg.speed = CAN_SPEED_1MBPS;
  CAN_cfg.tx_pin_id = GPIO_NUM_5;
  CAN_cfg.rx_pin_id = GPIO_NUM_4;
  CAN_cfg.rx_queue = xQueueCreate(rx_queue_size, sizeof(CAN_frame_t));
  // Init CAN Module
  ESP32Can.CANInit();
}

void loop() {

  CAN_frame_t rx_frame;
  unsigned long currentMillis = millis();

  // Receive next CAN frame from queue
  if (xQueueReceive(CAN_cfg.rx_queue, &rx_frame, 3 * portTICK_PERIOD_MS) == pdTRUE) {

    // Check if the received frame's ID matches the target ID
    if (rx_frame.MsgID == target_id) {

      if (rx_frame.FIR.B.FF == CAN_frame_std) {
        printf("New standard frame\n");
      }
      else {
        printf("New extended frame\n");
      }

      if (rx_frame.FIR.B.RTR == CAN_RTR) {
        printf(" RTR from 0x%08X, DLC %d\r\n", rx_frame.MsgID,  rx_frame.FIR.B.DLC);
      }
      else {
        printf(" from 0x%08X, DLC %d, Data ", rx_frame.MsgID,  rx_frame.FIR.B.DLC);
        for (int i = 0; i < rx_frame.FIR.B.DLC; i++) {
          printf("0x%02X ", rx_frame.data.u8[i]);
        }
        printf("\n");
      }
    }
  }
}