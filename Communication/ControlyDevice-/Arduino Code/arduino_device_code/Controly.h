#include "codes.h"
#include "deviceVariables.h"

#include "ArduinoJson.h"
#include <FastLED.h>

// DEBUG
#include <LiquidCrystal.h>


StaticJsonDocument<300> jsonDoc;

// Reading the serial and splitting it into two parts: code and payload
String entireSerial;
// When this string is empty it means there are no changes
String changes = "";
bool anyChanges = false;

//FUNCTION TO READ SERIAL
String readSerial();


// DEBUG
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);


void jsonUpdate();

//FUNCTION TO CONVERT FROM HEX TO DEC
unsigned int hexToDec(String hexString) {
  
  unsigned int decValue = 0;
  int nextInt;
  
  for (int i = 0; i < hexString.length(); i++) {
    
    nextInt = int(hexString.charAt(i));
    if (nextInt >= 48 && nextInt <= 57) nextInt = map(nextInt, 48, 57, 0, 9);
    if (nextInt >= 65 && nextInt <= 70) nextInt = map(nextInt, 65, 70, 10, 15);
    if (nextInt >= 97 && nextInt <= 102) nextInt = map(nextInt, 97, 102, 10, 15);
    nextInt = constrain(nextInt, 0, 15);
    
    decValue = (decValue * 16) + nextInt;
  }
  
  return decValue;
}

String returnFormat(int code, int id, String body) {
  return (String(code) + '*' + String(id) + '*' + body);
}

void handleAskForChanges(int code, int id, String _changes) {
  Serial.println(returnFormat(code, id, _changes));
}


// It will do every step to read and update from/to serial buffer. RETURNS 0 or 1: 0 = No changes from Controly, 1 = Changes
int serialUpdate(){
  // This will read and split serial buffer. It will the check for changes(if changes string is empty) and then
  String splittedSerial[3];
  entireSerial = readSerial();

  if (entireSerial == "NONE") {
    anyChanges = false;
    return 0;
  }

  // Format: < question_command >*< question_id >*< payload >
  String str = entireSerial;
  int StringCount = 0;
  while (str.length() > 0)
  {
    int index = str.indexOf('*');
    if (index == -1) // No * found
    {
      splittedSerial[StringCount++] = str;
      break;
    }
    else
    {
      splittedSerial[StringCount++] = str.substring(0, index);
      str = str.substring(index+1);
    }
  }

  int code = splittedSerial[0].toInt();
  int id = splittedSerial[1].toInt();
  String payload = splittedSerial[2];

  // Checking
  switch (code) {
    // 1. Are there any changes (ser == 02 - code for changes):
    case askForChanges:
      handleAskForChanges(code, id, changes);
      changes = "";

    // 2. Receiving changes
    case sendingChanges:
      // Here i have string(payload) looking like this: {"active_color": "FF0000", "state": true, ... }
      // 1. Deserialize JSON string
      auto err = deserializeJson(jsonDoc, splittedSerial[2]);

      // If there is error in parsing JSON
      if (err) {
        Serial.print(code);
        Serial.print('*');
        Serial.print(id);
        Serial.print('*');
        Serial.println(err.f_str());
        return 0;
      }

      // Here I should have deserialized JSON object/string
      // 2. Running device-specific json update function, which will update all device variables from JSON Object
      Serial.print(code);
      Serial.print('*');
      Serial.print(id);
      Serial.print('*');
      Serial.println("Uspesna posodobitev!");
      jsonUpdate();
      activeColors[0] = hexToDec(activeColor.substring(0,2));
      activeColors[1] = hexToDec(activeColor.substring(2,4));
      activeColors[2] = hexToDec(activeColor.substring(4,6));
      restColors[0] = hexToDec(restColor.substring(0,2));
      restColors[1] = hexToDec(restColor.substring(2,4));
      restColors[2] = hexToDec(restColor.substring(4,6));

      anyChanges = true;
  }
  return anyChanges;
}