#define lo8(x) ((x)&0xff)
#define hi8(x) ((x)>>8)

uint16_t crc_ccitt_update (uint16_t crc, uint8_t data) {
  data ^= lo8 (crc);
  data ^= data << 4;
  return ((((uint16_t)data << 8) | hi8 (crc)) ^ (uint8_t)(data >> 4)
    ^ ((uint16_t)data << 3));
}

inline uint16_t softcrc(uint16_t seed, uint8_t *data, uint16_t datalen) {
    for (uint16_t i=0; i<datalen; i++) {
        seed = crc_ccitt_update(seed,  data[i]);
    }
    return seed;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  byte byte_array[7] = {0x61, 0x62, 0x63, 0x64, 0x65, 0x66, 0x67};
  // put your main code here, to run repeatedly:
  uint16_t crc = softcrc(0, byte_array, 7);

  byte hi = crc >> 8;
  byte lo = crc & 0xFF;

  Serial.write(hi);
  Serial.write(lo);
}
