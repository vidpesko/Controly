#include "codes.h"

#include "ArduinoJson.h"

StaticJsonDocument<300> jsonDoc;

// Reading the serial and splitting it into two parts: code and payload
String entireSerial;
String splittedSerial[3];
int id;
int code;
String payload;

// When this string is empty it means there are no changes
String changes = "";

//FUNCTION TO READ SERIAL
String readSerial();

// Function to split serial into substrings
void splitSerial(String str, String (& strs) [3]);


void jsonUpdate();


String returnFormat(int code, int id, String body) {
  return (String(code) + '*' + String(id) + '*' + body);
}

void handleAskForChanges(int code, int id, String _changes) {
  Serial.println(returnFormat(code, id, _changes));
}

void handleSentChanges(int code, int id, String payload) {
  // Here i have string(payload) looking like this: {"active_color": "FF0000", "state": true, ... }
  // 1. Deserialize JSON string
  auto err = deserializeJson(jsonDoc, payload);
  // If there is error in parsing JSON
  if (err) {
    // Serial.print("......payload was: ");
    // Serial.print(splittedSerial[1]);
    // Serial.print("......and code was: ");
    // Serial.print(splittedSerial[0]);
    Serial.println(returnFormat(code, id, err.c_str()));
    return;
  }

  Serial.println(returnFormat(code, id, "Uspesna posodobitev!"));

  // Here I should have deserialized JSON object/string
  // 2. Running device-specific json update function, which will update all device variables from JSON Object
  jsonUpdate();
}

// It will do every step to read and update from/to serial buffer. RETURNS 0 or 1: 0 = No changes from Controly, 1 = Changes
int serialUpdate(){
  // This will read and split serial buffer. It will the check for changes(if changes string is empty) and then
  entireSerial = readSerial();

  if (entireSerial == "NONE") {
    return 0;
  }

  // Format: < question_command >*< question_id >*< payload >
  splitSerial(entireSerial, splittedSerial);
  code = splittedSerial[0].toInt();
  id = splittedSerial[1].toInt();
  payload = splittedSerial[2];

  // Checking
  switch (code) {
    // 1. Are there any changes (ser == 02 - code for changes):
    case askForChanges:
      handleAskForChanges(code, id, changes);
      changes = "";

    // 2. Receiving changes
    case sendingChanges:
      handleSentChanges(code, id, payload);
  }
}