#include <stdio.h>
#include <stdint.h>
#include <unistd.h>

uint16_t crc_ccitt_update(uint16_t crc, uint8_t data);
uint16_t softcrc(uint16_t seed, uint8_t *data, uint16_t datalen);
/* demo.c:  My first C program on a Linux */

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


int main(void)
{
  uint8_t byte_array[1024];
  int byte_array_len = 0;
  uint8_t byte;
  while(read(STDIN_FILENO, &byte, 1) > 0) {
    byte_array[byte_array_len] = byte;
    byte_array_len++;
  }

  //for (int i = 0; i < byte_array_len; i++) {
  //  printf("0x%02X\n", byte_array[i]);
  //}
  
  // put your main code here, to run repeatedly:
  uint16_t crc = softcrc(0, byte_array, byte_array_len);

  uint8_t hi = crc >> 8;
  uint8_t lo = crc & 0xFF;
  //printf("0x%02X", hi);
  //printf("0x%02X", lo);

  putchar(hi);
  putchar(lo);

  return 0;
}
 