#include <OneWire.h>
#include <Wire.h>
#include "HTU21D.h"
#include <DallasTemperature.h>
#include <LiquidCrystal.h>

//.........................................................constants


int t1 = 0;  //---Time = 0
String command = "";
boolean canLoop = false;
HTU21D myHumidity;  //---Humidity object


int tempPotPin = 0;
int tempOPin = 13;


//------------------------------------Setting up the two temp sensors--------------------------------


#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

DeviceAddress waterTemp = { 0x28, 0x1E, 0x52, 0x65, 0x05, 0x00, 0x00, 0x64 };
DeviceAddress cubeTemp = { 0x28, 0x47, 0x6F, 0x4D, 0x05, 0x00, 0x00, 0xD8 };


// .....................................................LCD display

LiquidCrystal monitor(30, 31, 32, 33, 34, 35);



//////////////////////////////    ............................setup


void setup(void) {

  Serial.begin(9600);
  sensors.begin();
  sensors.setResolution(waterTemp, 10);
  sensors.setResolution(cubeTemp, 10);
  
  pinMode(tempOPin, OUTPUT);
  
  myHumidity.begin();
  
  //....for the LCD
  monitor.begin(16, 2);
  monitor.print("tempC --- tempW");
  
  //Serial.println("time - tempW - tempC - tempH - humidity");


}
/*
void printTemperature(DeviceAddress deviceAddress) {
  
  float tempC = sensors.getTempC(deviceAddress);
  if (tempC == -127.00) {
    Serial.print("Error getting Temp");
  }
  else {
    return tempC
    //Serial.print(tempC);
    //Serial.print(" , ");
    //Serial.print(DallasTemperature::toFahrenheit(tempC));
  }
}
*/
////////////////////////////// ................................loop


void loop() {  
  
  
  monitor.setCursor(0, 1);
  sensors.requestTemperatures();
  
  //---Water Heater
  
  
  
  
  
  //---from humidity sensor
  
  float tempWater = sensors.getTempF(waterTemp);
  float tempCube = sensors.getTempF(cubeTemp);
  
  float humd = myHumidity.readHumidity();
  float tempH = (myHumidity.readTemperature()) * 1.8 + 32.0;
  
  
  //time
  
  //Serial.print(millis() / 1000);
  //Serial.print("   -   ");
  
  
  
  //Water TempC
  Serial.print(tempWater);
  //printTemperature(waterTemp);
  Serial.print("   -   ");

  
  //---cube temp
  
  Serial.print(tempCube);
  //printTemperature(cubeTemp);
  Serial.print("   -   ");
  
  
  
  //---tempC from humidity sensor
  Serial.print(tempH, 1);
  Serial.print("\n");
  
  delay(1000);
  monitor.print(tempWater);
  monitor.print("     ");
  monitor.print(tempCube);
}




