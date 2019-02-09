
#include <SPI.h>
#include <SFE_BMP180.h>
#include <Wire.h>
#include <SFE_LSM9DS0.h>
#include <TinyGPS++.h>


#define LSM9DS0_XM  0x1D // Would be 0x1E if SDO_XM is LOW
#define LSM9DS0_G   0x6B // Would be 0x6A if SDO_G is LOW
LSM9DS0 dof(MODE_I2C, LSM9DS0_G, LSM9DS0_XM);

SFE_BMP180 pressure;
TinyGPSPlus gps;

int cameraInterval = 20000; // ms
unsigned long lastCameraTime;
boolean cameraState = 0;

int communicationPin = 7;

void setup() {
  Serial1.begin(19200);
 
  //GPS Baud
  Serial3.begin(9600);
  
  pinMode(communicationPin, OUTPUT); 
  
  if (pressure.begin()){
  Serial1.println("BMP180 init success");
  }
  else
  {
    // Oops, something went wrong, this is usually a connection problem,
    // see the comments at the top of this sketch for the proper connections.

    Serial1.println("BMP180 init fail\n\n");
    while(1); // Pause forever.
  }
  
  
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

// The main loop, which sends the collected data via the Serial Radio to the ground station every 100 milliseconds
void loop() {
  
  while (Serial3.available() > 0){
    gps.encode(Serial3.read()); 
  }
  
  if (millis() > lastCameraTime + cameraInterval) {
    lastCameraTime = millis()
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
  Serial1.println(""); //Print new-line
  delay(100); // wait before sending next data-batch

}

void send_basics(){
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
  
  //Declares the variable used for storing the NTC data
  int NTC; //The analog input2
  
  //Reads the analog data from the corresponding sensor and assigns it to the variables declared above
  NTC = analogRead(A2);
  
  // Sends all the read data via the send_data_field function
  // Prints identifier
  Serial1.print("SGCanScience>");
  
  //Print Time
  send_data_field("Time", String(millis()));
  
  //Print NTC
  send_data_field("NTC", String(NTC));
  
  //Print BMP 180 pressure and temperature
  send_pressTemp();
  
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
  
  //GPS
  //Print Latitude
  send_data_field_float("Lat", gps.location.lat(), 6);
  
  //Print Longitude
  send_data_field_float("Lng", gps.location.lng(), 6);
  
  //Print  Satellites
  send_data_field("Sat", String(gps.satellites.value()));
}

void send_pressTemp() {
  
  char status;
  double T,P;
  status = pressure.startTemperature();
  
  if(status != 0) {
    delay(status);
    
    status = pressure.getTemperature(T);
      if (status != 0) {
      
      /*     
      Serial.print("Temperature:");
      Serial.print(T,2);
      Serial.print("|");
      */
      send_data_field_float("Temp", T, 2);
      
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
          send_data_field_float("Press", P, 2);
                
        }
      }
    }
  }     
}

void send_data_field(String key, String value) {
  Serial1.print(key + ":" + value + "|");
}

void send_data_field_float(String key, float value, int width) {
  Serial1.print(key + ":");
  Serial1.print(value, width);
  Serial1.print("|");
}
