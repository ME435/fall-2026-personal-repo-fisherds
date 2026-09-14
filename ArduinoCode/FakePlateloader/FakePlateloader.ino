String inputString = "";
bool isStringComplete = false;

void setup() {
  Serial.begin(19200);
  inputString.reserve(200);
}

void loop() {
  if (isStringComplete) {
    if (inputString.equals("RESET")) {
        delay(500);
      Serial.println("READY, SAGIAN PE Loader, ROM Ver. 1.1.6, 12APR2001");
    } else if (inputString.startsWith("MOVE")) {
        delay(3000);
      Serial.println("READY");
    } else if (inputString.startsWith("X-AXIS")) {
      Serial.println("READY");
    } else if (inputString.equals("GRIPPER OPEN")) {
      Serial.println("READY, OPEN");
    } else if (inputString.equals("GRIPPER CLOSE")) {
      Serial.println("READY, CLOSED, NOPLATE");
    } else if (inputString.equals("Z-AXIS EXTEND")) {
      Serial.println("READY, EXTENDED");
    } else if (inputString.equals("Z-AXIS RETRACT")) {
      Serial.println("READY, RETRACTED");
    } else {
      Serial.print("Unknown command --> ");
      Serial.println(inputString);
    }

    inputString = "";
    isStringComplete = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      isStringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}
