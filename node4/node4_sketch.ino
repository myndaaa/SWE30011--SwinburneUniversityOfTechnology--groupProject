#include <SPI.h>
#include <MFRC522.h>
#include <AccelStepper.h>

#define MotorInterfaceType 4
AccelStepper myStepper(MotorInterfaceType,5,7,6,8);

int ldr = A0;
int magnet_switch = 2;
int fan = 3;
int door_led = 4;
int SS_PIN = 10;
int RST_PIN = 9;
int accessGranted = 0;
bool breakIn = false;

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance
byte accessUID[4] = {0xEA, 0x27, 0xDD, 0xAE};
byte accessUID2[4] = {0xB3, 0x29, 0x8B, 0X1A};

char myData[30] = {0};
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  pinMode(ldr, INPUT);
  pinMode(magnet_switch, INPUT_PULLUP);
  pinMode(door_led, OUTPUT);
  pinMode(fan, OUTPUT);

  myStepper.setMaxSpeed(1000);
  myStepper.setAcceleration(100);
  myStepper.setSpeed(300);
  myStepper.moveTo(0);

  while (!Serial);    // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
  SPI.begin();      // Init SPI bus
  mfrc522.PCD_Init();   // Init MFRC522
  delay(4);       // Optional delay. Some board do need more time after init to be ready, see Readme
}

void loop() {
  // put your main code here, to run repeatedly:
  int light = analogRead(ldr);
  int door_state = digitalRead(magnet_switch);
  String msg = "";

  msg += String(light) + ":";
  msg += String(door_state) + ":";

  while (Serial.available() > 0){
    byte m = Serial.readBytesUntil('\n', myData, 30);
    myData[m] = '\0'; //null-byte
    int stepperDest = atoi(strtok(myData, ","));
    int fan_state = atoi(strtok(NULL, ","));
    
    if (myStepper.distanceToGo()== 0 ){
      myStepper.moveTo((stepperDest) * 2048);
    }
    switch(fan_state){
      case 0:
        digitalWrite(fan, LOW);
        break;
      case 1:
        digitalWrite(fan, HIGH);
        break;
    }
    
  }
  
  if ( accessGranted == 0){
      digitalWrite(door_led, LOW);
    }

  if (door_state == 1 && accessGranted == 0){
    breakIn = true;
  }
  
  msg += breakIn;
  if(accessGranted >0){
    accessGranted--;
  }  
  Serial.println(msg);
  myStepper.run();

  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }
    if ((mfrc522.uid.uidByte[0] == accessUID[0] && mfrc522.uid.uidByte[1] == accessUID[1] && mfrc522.uid.uidByte[2] == accessUID[2] && mfrc522.uid.uidByte[3] == accessUID[3]) || (mfrc522.uid.uidByte[0] == accessUID2[0] && mfrc522.uid.uidByte[1] == accessUID2[1] && mfrc522.uid.uidByte[2] == accessUID2[2] && mfrc522.uid.uidByte[3] == accessUID2[3])) {
      digitalWrite(door_led, HIGH);
      accessGranted = 500;
      breakIn = false;
    }
}
