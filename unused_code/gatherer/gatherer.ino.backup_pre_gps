/*
The Arduino C code that powers SG's 14/15 CanSat team's can.

By: SG CanSat 14/15
*/

// Both 9degree (I2C) and 3 serial measurements

#include <SPI.h> // Included for SFE_LSM9DS0 library
#include <Wire.h>
#include <SFE_LSM9DS0.h>

#define LSM9DS0_XM  0x1D // Would be 0x1E if SDO_XM is LOW
#define LSM9DS0_G   0x6B // Would be 0x6A if SDO_G is LOW
LSM9DS0 dof(MODE_I2C, LSM9DS0_G, LSM9DS0_XM);

void setup() {
//  pinMode(16, OUTPUT);  // init LED
//  pinMode(21, OUTPUT);  // init LED

  //Serial.begin(19200);  // init Serial USB
  Serial1.begin(19200);  // init Serial Radio
  
   // call it with declarations for sensor scales and data rates:
  uint16_t status = dof.begin(dof.G_SCALE_2000DPS,
                              dof.A_SCALE_16G, dof.M_SCALE_2GS);

  // make sure communication with 9degree sensor was successful.
  Serial1.print("LSM9DS0 WHO_AM_I's returned: 0x");
  Serial1.println(status, HEX);
  Serial1.println("Should be 0x49D4");
  Serial1.println();

  Serial.print("LSM9DS0 WHO_AM_I's returned: 0x");
  Serial.println(status, HEX);
  Serial.println("Should be 0x49D4");
  Serial.println();
  
}
// The main loop, which sends the collected data via the Serial Radio to the ground station every 200 milliseconds
void loop() {

  send_basics();           // Sends the collected data, which is read in the send_basics function
  delay(100);              // wait before sending next data-batch

}

void send_basics() {
  // Declares the variables and reads the "9 degrees of freedom"-data
  //Gyr data
  dof.readGyro();
  int GyrX = dof.gx;
  int GyrY = dof.gy;
  int GyrZ = dof.gz;

  //Acc data
  dof.readAccel();
  int AccX = dof.ax;
  int AccY = dof.ay;
  int AccZ = dof.az;

  //Mag data
  dof.readMag();
  int MagX = dof.mx;
  int MagY = dof.my;
  int MagZ = dof.mz;
  
  // Declares the variables used for storing the pressure, LM35, and NTC data
  // Temp & pressure data
  int Press; // the analog input0
  int LM35; // the analog input1
  int NTC; // the analog input2
  // Reads the analog data from the corresponding sensor and assigns it to the variables declared above
  Press = analogRead(A0); // reading the analog value port A0 Pressure
  LM35 = analogRead(A1); // reading the analog value port A1  LM35
  LM35 = analogRead(A1); // reading the analog value port A1  LM35 again. The first could be wrong
  NTC = analogRead(A2); // reading the analog value port A2  NTC

  //Sends all the read data via the send_data_field function
  //Print identifier
  Serial1.print("SGCanScience>");

  //Print Time
  send_data_field("Time", String(millis()));

  //Print Pressure
  send_data_field("Press", String(Press));

  //Print LM35
  send_data_field("LM35", String(LM35));

  //Print NTC
  send_data_field("NTC", String(NTC));
  
  //Print Gyr
  send_data_field("GyrX", String(GyrX));
  send_data_field("GyrY", String(GyrY));
  send_data_field("GyrZ", String(GyrZ));

  //Print Acc
  send_data_field("AccX", String(AccX));
  send_data_field("AccY", String(AccY));
  send_data_field("AccZ", String(AccZ));

  //Print Mag
  send_data_field("MagX", String(MagX));
  send_data_field("MagY", String(MagY));
  send_data_field("MagZ", String(MagZ));
  
  //Print new-line
  Serial1.println("");
  }

//The send_data_field function, which is called when sending data to the ground station
//Is used for formatting the data so the ground station is able to break the data in to the correct "blocks"
void send_data_field(String key, String value) {
  Serial1.print(key + ":" + value + "|");
}
