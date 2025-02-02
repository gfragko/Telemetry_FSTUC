#ifndef DTCManager_h
#define DTCManager_h

#include <Arduino.h>
#include <pgmspace.h> // For ESP32, use <pgmspace.h>

struct TroubleCode {
    uint16_t code;
    const char* description;
    const char* fix;
};

class DTCManager {
public:
    DTCManager();
    bool getTroubleCodeDetails(uint16_t code, String &description, String &fix);

public:
    static const TroubleCode troubleCodes[];
    static const int numTroubleCodes;
};

#endif