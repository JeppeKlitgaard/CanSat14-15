/* Linksprite */
 
byte incomingbyte;
int a=0x0000,j=0,k=0,count=0;                    //Read Starting address       
uint8_t MH,ML;
boolean EndFlag=0;
 
void SendResetCmd();
void SendTakePhotoCmd();
void SendReadDataCmd();
void StopTakePhotoCmd();
 
void setup()
{ 
  Serial.begin(38400);
  Serial3.begin(38400);
}
 
void loop() 
{
     SendResetCmd();
     delay(4000);                               //After reset, wait 2-3 second to send take picture command
 
     SendTakePhotoCmd();
     Serial.print("SWAP\n");
     delay(3000);

     byte a[32];
     boolean EndFlag=0;
 
     while(!EndFlag) {  
         j=0;
         k=0;
         count=0;
         SendReadDataCmd();
 
         delay(25);
          while(Serial3.available()>0)
          {
               incomingbyte=Serial3.read();
               k++;
               if((k>5)&&(j<32)&&(!EndFlag))
               {
               a[j]=incomingbyte;
               if((a[j-1]==0xFF)&&(a[j]==0xD9))      //Check if the picture is over
               EndFlag=1;                           
               j++;
	       count++;
               }
          }
 
          for(j=0;j<count;j++)
          {   if(a[j]<0x10)
              Serial.print("0");
              Serial.print(a[j],HEX);
              Serial.print(" ");
          }                                       //Send jpeg picture over the serial port
          Serial.println();
      }
}
 

//Send Reset command
void SendResetCmd()
{
      Serial3.write(0x56);
      Serial3.write((byte)0);
      Serial3.write(0x26);
      Serial3.write((byte)0);
}

//Send take picture command
void SendTakePhotoCmd()
{
      Serial3.write(0x56);
      Serial3.write((byte)0);
      Serial3.write(0x36);
      Serial3.write(0x01);
      Serial3.write((byte)0);  
}

//Read data
void SendReadDataCmd()
{
      MH=a/0x100;
      ML=a%0x100;
      Serial3.write(0x56);
      Serial3.write((byte)0);
      Serial3.write(0x32);
      Serial3.write(0x0c);
      Serial3.write((byte)0); 
      Serial3.write(0x0a);
      Serial3.write((byte)0);
      Serial3.write((byte)0);
      Serial3.write(MH);
      Serial3.write(ML);   
      Serial3.write((byte)0);
      Serial3.write((byte)0);
      Serial3.write((byte)0);
      Serial3.write(0x20);
      Serial3.write((byte)0);  
      Serial3.write(0x0a);
      a+=0x20;                            //address increases 32£¬set according to buffer size
}

void StopTakePhotoCmd()
{
      Serial3.write(0x56);
      Serial3.write((byte)0);
      Serial3.write(0x36);
      Serial3.write(0x01);
      Serial3.write(0x03);        
}

