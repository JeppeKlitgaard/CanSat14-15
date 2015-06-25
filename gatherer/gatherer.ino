#include <util/crc16.h>

#include <SPI.h>
#include <SFE_BMP180.h>
#include <Wire.h>
#include <SFE_LSM9DS0.h>
#include <TinyGPS++.h>


#define LSM9DS0_XM  0x1D // Would be 0x1E if SDO_XM is LOW
#define LSM9DS0_G   0x6B // Would be 0x6A if SDO_G is LOW
LSM9DS0 dof(MODE_I2C, LSM9DS0_G, LSM9DS0_XM);

inline uint16_t softcrcXMODEM(uint16_t seed, uint8_t *data, uint16_t datalen) {
    for (uint16_t i=0; i<datalen; i++) {
        seed = _crc_xmodem_update(seed,  data[i]);
    }
    return seed;
}

SFE_BMP180 pressure;
TinyGPSPlus gps;

int cameraInterval = 20000; // ms
unsigned long lastCameraTime;
boolean cameraState = 0;

int communicationPin = 15;
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream

const byte magic = 0xFF;

const int s = 256;
int to_send_next_pos = 0;
byte to_send[s];

uint16_t crc;

union {
  double d;
  int i;
  unsigned long ul;
  uint32_t u32;
  unsigned char b[4];
} ba;
//
//uint16_t crc16(byte* data_p, byte length){
//    unsigned char x;
//    unsigned short crc = 0xFFFF;
//
//    while (length--){
//        x = crc >> 8 ^ *data_p++;
//        x ^= x>>4;
//        crc = (crc << 8) ^ ((unsigned short)(x << 12)) ^ ((unsigned short)(x <<5)) ^ ((unsigned short)x);
//    }
//    return crc;
//}

void flush_buf() {
  int data_size;

  Serial1.print("SGCan");
  Serial1.print("1");  // version

  data_size = to_send_next_pos + 2; // CRC
  Serial1.write((byte)data_size);

  for (int k = 0; k < to_send_next_pos; k++) {
    Serial1.write((byte) to_send[k]);
  }

  crc = softcrcXMODEM(0, to_send, to_send_next_pos);

  byte hi = crc >> 8;
  byte lo = crc & 0xFF;

  Serial1.write(hi);
  Serial1.write(lo);

  Serial1.write(magic);

  Serial1.print("\n");
  Serial1.flush();
  
  to_send_next_pos = 0;
}

void add_double(double d) {
  ba.d = d;
  for (int k = 0; k < sizeof(double); k++) {
    to_send[to_send_next_pos] = (char) ba.b[k];
    to_send_next_pos++;
  }
}

void add_int(int i) {
  ba.i = i;
  for (int k = 0; k < sizeof(int); k++) {
    to_send[to_send_next_pos] = (char) ba.b[k];
    to_send_next_pos++;
  }
}

void add_unsigned_long(unsigned long ul) {
  ba.ul = ul;
  for (int k = 0; k < sizeof(long); k++) {
    to_send[to_send_next_pos] = (char) ba.b[k];
    to_send_next_pos++;
  }
}

void add_uint32(uint32_t u32) {
  ba.u32 = u32;
  for (int k = 0; k < sizeof(uint32_t); k++) {
    to_send[to_send_next_pos] = (char) ba.b[k];
    to_send_next_pos++;
  }
}

=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

void setup() {
  Serial1.begin(19200);
 
  //GPS Baud
  Serial3.begin(9600);
  
  pinMode(communicationPin, OUTPUT); 

  pressure.begin();
  // if (pressure.begin()){
  // Serial1.println("BMP180 init success");
  // }
  // else
  // {
  //   // Oops, something went wrong, this is usually a connection problem,
  //   // see the comments at the top of this sketch for the proper connections.

  //   Serial1.println("BMP180 init fail\n\n");
  //   while(1); // Pause forever.
  // }
  
  
  // call it with declarations for sensor scales and data rates:
  uint16_t status = dof.begin(dof.G_SCALE_2000DPS,
                              dof.A_SCALE_16G, dof.M_SCALE_2GS);

  // make sure communication with 9degree sensor was successful.
  // Serial1.print("LSM9DS0 WHO_AM_I's returned: 0x");
  // Serial1.println(status, HEX);
  // Serial1.println("Should be 0x49D4");
  // Serial1.println();

  // Serial.print("LSM9DS0 WHO_AM_I's returned: 0x");
  // Serial.println(status, HEX);
  // Serial.println("Should be 0x49D4");
  // Serial.println();
  
}

// The main loop, which sends the collected data via the Serial Radio to the ground station every 100 milliseconds
void loop() {
  
  while (Serial3.available() > 0){
    gps.encode(Serial3.read()); 
  }
  
  if (millis() > lastCameraTime + cameraInterval) {
    lastCameraTime = millis();
    if (cameraState == 0) {
      cameraState = 1;
      digitalWrite(communicationPin, HIGH);
    } else {
      cameraState = 0;
      digitalWrite(communicationPin, LOW);
    }
  }
  send_basics(); // Sends the collected data, which is read in the send_basics function
 /* 
  if(Serial3.available()){
    Serial.write(Serial3.read());
  }
 */
  delay(100); // wait before sending next data-batch

}

void send_basics(){
  // Declares the variables and reads the "9 degrees of freedom"-data
  //Gyr data
  dof.readGyro();
  
  add_int(dof.gx);
  add_int(dof.gy);
  add_int(dof.gz);

  //Acc data
  dof.readAccel();

  add_int(dof.ax);
  add_int(dof.ay);
  add_int(dof.az);

  //Mag data
  dof.readMag();

  add_int(dof.mx);
  add_int(dof.my);
  add_int(dof.mz);

  // NTC
  add_int(analogRead(A2));
  
  //Print Time
  add_unsigned_long(millis());
  
  //Print BMP 180 pressure and temperature
  // Temperature - double
  // Pressure - double
  send_press_temp();
  
  //GPS
  add_double(gps.location.lat());
  add_double(gps.location.lng());

  add_double(gps.altitude.meters());

  add_double(gps.course.deg());

  add_unsigned_long(gps.hdop.value());  // signed, but it doesn't matter here, only on the groundstation.

  add_uint32(gps.satellites.value());

  flush_buf();
}

void send_press_temp() {
  
  char status;
  double T,P;
  status = pressure.startTemperature();
  
  if(status != 0) {
    delay(status);
    
    status = pressure.getTemperature(T);
      if (status != 0) {
      
          
//      Serial1.print("Temperature:");
//      Serial1.print(T,2);
//      Serial1.print("|");
      
      
      status = pressure.startPressure(3);
    
      if(status != 0) {
        delay(status);
        
      
        status = pressure.getPressure(P,T);
        if (status != 0) {
          /*
          Serial.print("Pressure:");
          Serial.print(P,2);
          Serial.print("|");
          */
          
                
        }
      }
    }
  }
  add_double(T);
  add_double(P);
}
