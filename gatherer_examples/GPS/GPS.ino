#include <Wire.h>
#include <TinyGPS++.h>

TinyGPSPlus gps;

void setup() {
  Serial.begin(19200);
  Serial3.begin(9600);
}

void loop(){
  while (Serial3.available() > 0){
    gps.encode(Serial3.read());
  }
  /*
  if(gps.location.isUpdated()){
    Serial.println(gps.location.lat(), 6);
  }
  
  if(gps.location.isUpdated()){
    Serial.println(gps.location.lng(), 6);
  }
  */
  
  Serial.print("SGCanScience>Latitude:");
  Serial.print(gps.location.lat(), 6);
  Serial.print("|Longitude:");
  Serial.print(gps.location.lng(), 6);
  Serial.print("|Satellites:");
  Serial.print(gps.satellites.value());
  Serial.println("");
  
  delay(100);
}
