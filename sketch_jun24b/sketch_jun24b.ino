//FastCRC
//Quick'n dirty Benchmark
//
//(c) Frank Boesing 2014

#include <util/crc16.h>
#include <FastCRC.h>

#define Ser Serial
#define BUFSIZE 16384


FastCRC8 CRC8;
FastCRC16 CRC16;
FastCRC32 CRC32;

uint8_t buf[BUFSIZE];


// Supporting functions for Software CRC

inline uint16_t softcrc(uint16_t seed, uint8_t *data, uint16_t datalen) {
    for (uint16_t i=0; i<datalen; i++) {
        seed = _crc16_update(seed,  data[i]);
    }
    return seed;
}

inline uint16_t softcrcIbutton(uint16_t seed, uint8_t *data, uint16_t datalen) {
    for (uint16_t i=0; i<datalen; i++) {
        seed = _crc_ibutton_update(seed,  data[i]);
    }
    return seed;
}

inline uint16_t softcrcCCIT(uint16_t seed, uint8_t *data, uint16_t datalen) {
    for (uint16_t i=0; i<datalen; i++) {
        seed = _crc_ccitt_update(seed,  data[i]);
    }
    return seed;
}

inline uint16_t softcrcXMODEM(uint16_t seed, uint8_t *data, uint16_t datalen) {
    for (uint16_t i=0; i<datalen; i++) {
        seed = _crc_xmodem_update(seed,  data[i]);
    }
    return seed;
}


void setup() {
int time;
uint32_t crc;


  Ser.begin(115200);
 // while (!Ser) {};
  //Fill array with data
  for (int i=0; i<BUFSIZE; i++) {
    buf[i] = (i+1) & 0xff;
  }

  Serial.println("\r\nXMODEM 16-Bit CRC:");
  Serial.flush();

  Serial.println("HW");
  time = micros();
  crc = CRC16.xmodem(buf, BUFSIZE);
  time = micros() - time;
  Serial.print(crc);
  Serial.print(time);
  Serial.flush();

  Serial.println("SW");
  time = micros();
  crc = softcrcXMODEM(0, buf, BUFSIZE);
  time = micros() - time;
  Serial.print(crc);
  Serial.print(time);
  Serial.flush();

}

void loop() {
  delay(1000);
}
