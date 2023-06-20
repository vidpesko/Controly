// SERIAL

// FUNCTION TO READ SERIAL
String readSerial() {
  if (!Serial.available()) {
    return "NONE";
  }
  String x = Serial.readString();
  return x;
}

// Function to split serial into substrings
void splitSerial(String str, String (& strs) [3]) {
  // lcd.setCursor(0, 1);
  // lcd.print("str: ");
  // lcd.print(str);
  int StringCount = 0;
  while (str.length() > 0)
  {
    int index = str.indexOf('*');
    if (index == -1) // No * found
    {
      strs[StringCount++] = str;
      break;
    }
    else
    {
      strs[StringCount++] = str.substring(0, index);
      str = str.substring(index+1);
    }
  }
}