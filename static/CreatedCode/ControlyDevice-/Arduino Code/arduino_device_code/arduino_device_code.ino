#include "Controly.h"
#include "deviceVariables.h"

// For debugging reasons:
#include <LiquidCrystal.h>

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);


// Defining needed PINS for device
#define LED 13


// Here are defined all device variables, that can be change from Controly
String activeColor = "00FF00";
String restColor = "00FF00";
String animation = "basic";
bool state = true;


void setup() {
  // Again, for debugging reasons
  lcd.begin(16, 2);

  // Starting the serial connection
  Serial.begin(9600);

  // Defining PINs modes
  pinMode(LED, OUTPUT);
}

void loop() {
  serialUpdate();

  // Actual code:
  if (state){
    digitalWrite(LED, HIGH);
  } else {
    digitalWrite(LED, LOW);
    changes = "Stop";
  }
}




