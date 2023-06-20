// SERIAL

// FUNCTION TO READ SERIAL
String readSerial() {
  if (!Serial.available()) {
    return "NONE";
  }
  String x = Serial.readStringUntil('\n');
  return x;
}