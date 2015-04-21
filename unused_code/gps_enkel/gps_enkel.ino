void setup()
{
  Serial.begin(19200);
  Serial3.begin(4800); // GPS-datahastighet er 9600
}
 
void get_gps()
{
  char string[100];      // En streng det leses inn i
 
  while (Serial3.available())  // venter på info fra GPS
  {
  for (int i = 0; i<100; i++)
  {
    string[i]=Serial3.read();  // Min erfaring var at det ikke kan skrives ut mens det leses inn. Utskrift tar for lang tid og man mister info fra GPS mens serial.print skriver
  }
//  Skriver ut hele strengen hvis det er behov for det.
  for (int i=0;i<100;i++)
    Serial.print(string[i]);
  Serial.println();
  // if (strncmp(string,"$GPRMC",6)==0)  // sjekker om de første 6 tegnene i strengen er $GPRMC
  // {
  //   for (int i=19; i<29;i++)
  //     Serial.print(string[i]);  // skriver ut nordkoordinatene
  //   Serial.print("N  ");
  //   for (int i=33; i<43; i++)
  //     Serial.print(string[i]);  // skriver ut øst-koordinater. Vil blir helt feil dersom det vest-koordinater som oppgis fra GPS
  //   Serial.println("E  ");
  // }
  }
 
}
void loop()
{
  get_gps();
  delay(1000);
}