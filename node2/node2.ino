int const BUZZER = 4;
//  Motor A
int const ENA = 10;  
int const INA = 12;
//  Motor B
int const ENB = 11;  
int const INB = 13;

//Ultrasonic sensor
const int trigPin = 8;
const int echoPin = 9;

int duration;
int stop;
int distance;
bool flag = true;
String MotorA;
String MotorB;
String alarmInstruction;
String moveInstruction;

String incomingByte;

#include <DHT.h>

#define DHTPIN 7    // Pin where the temp sensor is connected
#define DHTTYPE DHT11   // DHT 11

DHT dht(DHTPIN, DHTTYPE);

//===============================================================================
//  Initialization
//===============================================================================
void setup()
{
  pinMode(ENA, OUTPUT);   // set all the motor control pins to outputs
  pinMode(ENB, OUTPUT);
  pinMode(INA, OUTPUT);
  pinMode(INB, OUTPUT);

  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input

  pinMode(BUZZER, OUTPUT); // Sets the buzzer
  
  dht.begin(); // Temperature sensor
  
  Serial.begin(9600);     // Set comm speed for serial monitor messages
  Move(0,0, 100);
}

void loop()
{
  // Printing out the temp and humidity

  // Make buzzer sound
  digitalWrite(BUZZER, LOW);
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2;
  // Prints the distance on the Serial Monitor
  if(distance < 30 && flag && stop == 1)
  {
    Serial.println(distance);
    delay(50);
    flag = false;

  }
  else if(distance > 30 && distance <1000 && !flag)
  {
    flag = true;
  }
  
  if (Serial.available() > 0) {
    incomingByte = Serial.readString();
    
    /*Serial.print("Receive: ");
    Serial.print (incomingByte);*/

  }

  switch (incomingByte.toInt()) {
    case 1: //move forward
      Move (255, 255, distance);
      break;
    case 2: //turn
      Move (255, 0, distance);
      break;
    case 3: //patrol
      Patrol();
      break;
    case 4: //stop
      Move (0, 0,  distance);
      break;
    case 5: //buzzer off
      digitalWrite(BUZZER, LOW);
      break;
    case 6: //buzzer on
      digitalWrite(BUZZER, HIGH);
      break;
  }
}

void Patrol() {
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();

    // Check if any reads failed and exit early (to try again).
    if (isnan(humidity) || isnan(temperature)) {
      return;
    } 
  //Assuming starting at living room
    Move(255, 255, distance);
    delay (5000);
    Move(255, 0, distance);
    delay (1000);

    //taking temperature for kitchen
    Serial.print(temperature);
    Serial.print(":");
    Serial.println(humidity);

    //moving to living room
    Move(255, 255, distance);
    delay (5000);
    Move(255, 0, distance);
    delay(1000);

    //taking temperature for living room
    Serial.print(temperature);
    Serial.print(":");
    Serial.println(humidity);
}


void Move (int MotorA, int MotorB, int Distance)
{
  stop = 0;
  if (MotorA > 0 && Distance > 30) {
    digitalWrite(INA, HIGH);
    analogWrite (ENA, MotorA);
    stop = 1;
  }
  else if (MotorA < 0) {
    digitalWrite(INA, LOW);
    analogWrite (ENA, MotorA*-1);
    stop = 1;
  }

  else {
    digitalWrite (INA, HIGH);
    analogWrite (ENA, 0);
  }

  if (MotorB > 0 && Distance > 30) {
    digitalWrite(INB, HIGH);
    analogWrite (ENB, MotorB);
    stop = 1;
  }
  else if (MotorB < 0) {
    digitalWrite(INB, LOW);
    analogWrite (ENB, MotorB*-1);
    stop = 1;
  }

  else {
    digitalWrite (INB, HIGH);
    analogWrite (ENB, 0);
  }
}


String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
