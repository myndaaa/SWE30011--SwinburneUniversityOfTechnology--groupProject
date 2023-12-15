#include <MQ135.h>
#include <DHT.h>

#define DHTPIN 7
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const int rainSensorPin = 2;
const int relayPin = 9;
const int mq135Pin = A0;
const int waterLevelPin = 4; 
const int soilMoisturePin = A1; 


MQ135 gasSensor = MQ135(mq135Pin); //smoke detector
int motorState = 0; // Motor state from the database

void setup() {
  
  pinMode(rainSensorPin, INPUT);
  pinMode(relayPin, OUTPUT);
  pinMode(waterLevelPin, INPUT);
  pinMode(mq135Pin,INPUT);
  pinMode(soilMoisturePin, INPUT);

  Serial.begin(9600);// Initialize serial communication
  dht.begin();//initializing dht11

}

void loop() {
  int soilMoistureValue = analogRead(soilMoisturePin);
  int mappedMoisture = map(soilMoistureValue, 0, 1023, 0, 100); //the original output ranges from 0 to 1023, so mapping it for ease
  int rainValue = digitalRead(rainSensorPin);
  int waterLevelState = digitalRead(waterLevelPin);
  float smoke = gasSensor.getPPM();  
  
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Check the motor state from the database
  if (Serial.available() > 0) {
    motorState = Serial.read() - '0'; // Read single digit from serial and convert to integer
  }

  // Control the relay based on conditions
  if (motorState == 1 || (mappedMoisture < 40 )) {
    digitalWrite(relayPin, HIGH); // Turn on relay
  } else {
    digitalWrite(relayPin, LOW && rainValue == HIGH); // Turn off relay
  }
  
  
  Serial.print(temperature);
  Serial.print(",");
  Serial.print(mappedMoisture);
  Serial.print(",");
  Serial.print(smoke);
  Serial.print(",");
  Serial.print(waterLevelState);
  Serial.print(",");
  Serial.print(rainValue);
  Serial.println();

  delay(1000);       
}



