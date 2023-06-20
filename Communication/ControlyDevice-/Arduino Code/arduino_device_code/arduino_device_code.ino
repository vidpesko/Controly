#include "Controly.h"

// Defining needed PINS for device (sensors, leds, ...)
#define LED_DATA_PIN 13
#define NUM_LEDS 139


CRGB leds[NUM_LEDS];


void setup() {
  // Starting the serial connection
  Serial.begin(9600);

  // FastLED.addLeds<WS2811, DATA_PIN>(leds, NUM_LEDS);
  FastLED.addLeds<WS2811, LED_DATA_PIN, BRG>(leds, NUM_LEDS);

  // DEBUG
  // lcd.begin(16, 2);
}

void loop() {
  serialUpdate();

  if (!anyChanges) {return;}

  // Actual code:
  if (state){
    turnOnFromMiddle(activeColors, leds, NUM_LEDS);
  } else {
    turnOffFromMiddle(true, leds, NUM_LEDS);
  }
}