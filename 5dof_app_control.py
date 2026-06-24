#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <BluetoothSerial.h>
#include <Adafruit_PWMServoDriver.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

BluetoothSerial SerialBT;
Adafruit_PWMServoDriver pwm(0x40);

#define OLED_WIDTH 128
#define OLED_HEIGHT 64

#define OLED_CLK 18
#define OLED_MOSI 23
#define OLED_RST 4
#define OLED_DC 13
#define OLED_CS 14

Adafruit_SSD1306 display(
  OLED_WIDTH,
  OLED_HEIGHT,
  &SPI,
  OLED_DC,
  OLED_RST,
  OLED_CS
);

#define J1 0
#define J2 1
#define J3 2
#define J4 3
#define J5 4
#define GRIPPER 5

#define SERVOMIN 100
#define SERVOMAX 520

int j1Offset = 90;
int j2Offset = 95;
int j3Offset = 90;
int j4Offset = 90;
int j5Offset = 90;
int gripOffset = 90;

float c1 = 0;
float c2 = 0;
float c3 = 0;
float c4 = 0;
float c5 = 0;
float cg = 50;

float home1 = 0;
float home2 = 0;
float home3 = 0;
float home4 = 0;
float home5 = 0;
float homeG = 50;

const uint16_t motionIntervalMs = 20;
const float armSpeedDegPerSec = 28.0;
const float gripSpeedDegPerSec = 45.0;

const float jogStep = 4.0;
const float wristStep = 5.0;

bool stopRequested = false;

int angleToPulse(float angle) {
  angle = constrain(angle, 0, 180);
  return map((int)angle, 0, 180, SERVOMIN, SERVOMAX);
}

float smootherStep(float x) {
  x = constrain(x, 0.0, 1.0);
  return x * x * x * (x * (x * 6 - 15) + 10);
}

void showOLED(String line1, String line2 = "", String line3 = "") {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);

  display.setCursor(0, 0);
  display.println("5DOF ROBOT ARM");

  display.drawLine(0, 10, OLED_WIDTH, 10, SSD1306_WHITE);

  display.setCursor(0, 18);
  display.println(line1);

  display.setCursor(0, 32);
  display.println(line2);

  display.setCursor(0, 46);
  display.println(line3);

  display.display();
}

void writeServos() {
  pwm.setPWM(J1, 0, angleToPulse(c1 + j1Offset));
  pwm.setPWM(J2, 0, angleToPulse(c2 + j2Offset));
  pwm.setPWM(J3, 0, angleToPulse(c3 + j3Offset));
  pwm.setPWM(J4, 0, angleToPulse(c4 + j4Offset));
  pwm.setPWM(J5, 0, angleToPulse(c5 + j5Offset));
  pwm.setPWM(GRIPPER, 0, angleToPulse(cg + gripOffset));
}

String readBluetoothCommand() {
  if (!SerialBT.available()) return "";

  String cmd = "";
  char first = SerialBT.read();

  if (first == '\n' || first == '\r') return "";

  cmd += first;

  unsigned long start = millis();

  while (millis() - start < 25) {
    while (SerialBT.available()) {
      char c = SerialBT.read();

      if (c == '\n' || c == '\r') {
        cmd.trim();
        return cmd;
      }

      cmd += c;
      start = millis();
    }
  }

  cmd.trim();
  return cmd;
}

void checkStopCommand() {
  if (!SerialBT.available()) return;

  String cmd = readBluetoothCommand();
  cmd.toUpperCase();

  if (cmd == "T" || cmd == "STOP") {
    stopRequested = true;
    showOLED("STOP REQUESTED");
  }
}

bool moveRobot(float t1, float t2, float t3, float t4, float t5, String status) {
  float s1 = c1;
  float s2 = c2;
  float s3 = c3;
  float s4 = c4;
  float s5 = c5;

  t1 = constrain(t1, -85, 85);
  t2 = constrain(t2, -60, 45);
  t3 = constrain(t3, -20, 65);
  t4 = constrain(t4, -45, 45);
  t5 = constrain(t5, -45, 45);

  float maxDelta = max(abs(t1 - s1), abs(t2 - s2));
  maxDelta = max(maxDelta, abs(t3 - s3));
  maxDelta = max(maxDelta, abs(t4 - s4));
  maxDelta = max(maxDelta, abs(t5 - s5));

  uint32_t durationMs = max(
    (uint32_t)250,
    (uint32_t)((maxDelta / armSpeedDegPerSec) * 1000.0)
  );

  uint32_t startTime = millis();
  uint32_t lastStep = 0;

  showOLED(status, "Smooth motion");

  while (true) {
    checkStopCommand();

    if (stopRequested) {
      writeServos();
      return false;
    }

    uint32_t now = millis();

    if (now - lastStep >= motionIntervalMs) {
      lastStep = now;

      float progress = (float)(now - startTime) / (float)durationMs;
      float e = smootherStep(progress);

      c1 = s1 + (t1 - s1) * e;
      c2 = s2 + (t2 - s2) * e;
      c3 = s3 + (t3 - s3) * e;
      c4 = s4 + (t4 - s4) * e;
      c5 = s5 + (t5 - s5) * e;

      writeServos();

      if (progress >= 1.0) break;
    }
  }

  c1 = t1;
  c2 = t2;
  c3 = t3;
  c4 = t4;
  c5 = t5;

  writeServos();
  return true;
}

bool moveGripper(float target, String status) {
  float start = cg;

  target = constrain(target, -30, 50);

  float delta = abs(target - start);

  uint32_t durationMs = max(
    (uint32_t)250,
    (uint32_t)((delta / gripSpeedDegPerSec) * 1000.0)
  );

  uint32_t startTime = millis();
  uint32_t lastStep = 0;

  showOLED(status, "Gripper moving");

  while (true) {
    checkStopCommand();

    if (stopRequested) {
      writeServos();
      return false;
    }

    uint32_t now = millis();

    if (now - lastStep >= motionIntervalMs) {
      lastStep = now;

      float progress = (float)(now - startTime) / (float)durationMs;
      float e = smootherStep(progress);

      cg = start + (target - start) * e;
      writeServos();

      if (progress >= 1.0) break;
    }
  }

  cg = target;
  writeServos();
  return true;
}

bool smoothDelay(uint32_t ms, String status) {
  showOLED(status);

  uint32_t start = millis();

  while (millis() - start < ms) {
    checkStopCommand();

    if (stopRequested) return false;

    delay(10);
  }

  return true;
}

bool goHomeSlowly() {
  stopRequested = false;

  if (!moveRobot(home1, home2, home3, home4, home5, "GOING HOME")) return false;
  if (!moveGripper(homeG, "HOME GRIPPER")) return false;

  showOLED("HOME READY");
  return true;
}

bool pickAndPlaceOnce(int cycleNumber) {
  showOLED("AUTO MODE", "Cycle " + String(cycleNumber), "Starting");

  if (!moveRobot(0, 0, 0, 0, 0, "HOME")) return false;
  if (!moveGripper(50, "OPEN GRIPPER")) return false;
  if (!smoothDelay(700, "READY")) return false;

  if (!moveRobot(40, -10, 10, 0, -15, "MOVE ABOVE P1")) return false;
  if (!smoothDelay(500, "APPROACHING")) return false;

  if (!moveRobot(80, -10, 40, 0, -30, "FINAL ABOVE P1")) return false;
  if (!smoothDelay(500, "ALIGN P1")) return false;

  if (!moveRobot(80, -45, 80, 0, -30, "LAND AT P1")) return false;
  if (!smoothDelay(700, "PICK POINT")) return false;

  if (!moveGripper(-30, "CLOSE GRIPPER")) return false;
  if (!smoothDelay(700, "OBJECT GRABBED")) return false;

  if (!moveRobot(80, -10, 10, 0, -30, "LIFT OBJECT")) return false;
  if (!smoothDelay(500, "LIFTED")) return false;

  if (!moveRobot(40, -10, 10, 0, -30, "MOVE CENTER")) return false;
  if (!smoothDelay(500, "CENTER")) return false;

  if (!moveRobot(0, -10, 10, 0, -30, "MOVE ABOVE P2")) return false;
  if (!smoothDelay(500, "ALIGN P2")) return false;

  if (!moveRobot(0, -45, 40, 0, -30, "LAND AT P2")) return false;
  if (!smoothDelay(700, "PLACE POINT")) return false;

  if (!moveRobot(0, -45, 40, 15, -30, "WRIST RIGHT")) return false;
  if (!smoothDelay(300, "WRIST")) return false;

  if (!moveRobot(0, -45, 40, -15, -30, "WRIST LEFT")) return false;
  if (!smoothDelay(300, "WRIST")) return false;

  if (!moveRobot(0, -45, 40, 0, -30, "WRIST CENTER")) return false;
  if (!smoothDelay(300, "WRIST")) return false;

  if (!moveGripper(50, "OPEN DROP")) return false;
  if (!smoothDelay(700, "OBJECT RELEASED")) return false;

  if (!moveRobot(0, -10, 10, 0, -10, "MOVE UP")) return false;
  if (!smoothDelay(500, "CLEAR")) return false;

  if (!moveRobot(0, 0, 0, 0, 0, "RETURN HOME")) return false;
  if (!smoothDelay(700, "CYCLE DONE")) return false;

  return true;
}

void runThreePickPlaceActions() {
  stopRequested = false;

  for (int i = 1; i <= 3; i++) {
    if (!pickAndPlaceOnce(i)) {
      showOLED("AUTO STOPPED", "Cycle " + String(i));
      return;
    }
  }

  showOLED("AUTO COMPLETE", "3 actions done", "BT control ready");
}

void jogArm(float dx, float dy, float dz, float da) {
  stopRequested = false;

  float t1 = c1;
  float t2 = c2;
  float t3 = c3;
  float t4 = c4;
  float t5 = c5;

  t1 += dx * jogStep;

  t2 += dz * jogStep;
  t3 -= dz * jogStep;

  t2 -= dy * jogStep;
  t3 += dy * jogStep;

  t4 += da * wristStep;

  moveRobot(t1, t2, t3, t4, t5, "JOYSTICK MOVE");
}

void setGripperPercent(int percent) {
  percent = constrain(percent, 0, 100);

  float target = 50.0 - ((float)percent * 80.0 / 100.0);

  moveGripper(target, "GRIP " + String(percent) + "%");
}

void handleBluetoothCommand(String cmd) {
  cmd.trim();
  cmd.toUpperCase();

  if (cmd.length() == 0) return;

  if (cmd == "W") {
    jogArm(0, 1, 0, 0);
  } else if (cmd == "S") {
    jogArm(0, -1, 0, 0);
  } else if (cmd == "D") {
    jogArm(1, 0, 0, 0);
  } else if (cmd == "A") {
    jogArm(-1, 0, 0, 0);
  } else if (cmd == "I") {
    jogArm(0, 0, 1, 0);
  } else if (cmd == "K") {
    jogArm(0, 0, -1, 0);
  } else if (cmd == "J") {
    jogArm(0, 0, 0, -1);
  } else if (cmd == "M") {
    jogArm(0, 0, 0, 1);
  } else if (cmd == "F") {
    setGripperPercent(100);
  } else if (cmd == "G") {
    setGripperPercent(0);
  } else if (cmd.startsWith("M")) {
    int percent = cmd.substring(1).toInt();
    setGripperPercent(percent);
  } else if (cmd == "V") {
    home1 = c1;
    home2 = c2;
    home3 = c3;
    home4 = c4;
    home5 = c5;
    homeG = cg;
    showOLED("HOME SAVED", "Current position");
  } else if (cmd == "P") {
    goHomeSlowly();
  } else if (cmd == "T" || cmd == "STOP") {
    stopRequested = true;
    showOLED("STOPPED");
  } else if (cmd == "START" || cmd == "AUTO") {
    runThreePickPlaceActions();
  } else {
    showOLED("UNKNOWN COMMAND", cmd);
  }
}

void setup() {
  Serial.begin(9600);

  SerialBT.begin("ROBOT_ARM");
  SerialBT.setTimeout(25);

  Wire.begin(21, 22);

  SPI.begin(OLED_CLK, -1, OLED_MOSI, OLED_CS);

  if (!display.begin(SSD1306_SWITCHCAPVCC)) {
    while (true) {
      delay(100);
    }
  }

  display.setRotation(3);
  showOLED("BOOTING", "Bluetooth optional");

  pwm.begin();
  pwm.setPWMFreq(50);

  delay(1000);

  writeServos();

  goHomeSlowly();

  runThreePickPlaceActions();

  showOLED("READY", "WASD control", "BT: ROBOT_ARM");
}

void loop() {
  String cmd = readBluetoothCommand();

  if (cmd.length() > 0) {
    handleBluetoothCommand(cmd);
  }

  delay(10);
}
