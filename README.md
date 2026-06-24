# 5DOF Robotic Arm with ESP32, Bluetooth Control and OLED Interface

## Overview

This project presents a 5 Degrees of Freedom (5DOF) robotic arm controlled using an ESP32 microcontroller, PCA9685 servo driver, Bluetooth communication, and an OLED display interface. The robotic arm performs smooth automated pick-and-place operations while also supporting real-time wireless manual control through a Bluetooth-enabled smartphone application.

The system incorporates trajectory smoothing using a quintic smooth-step motion profile to achieve professional, jerk-free movements during object manipulation.

---

## Features

* 5DOF Robotic Arm
* ESP32 Wireless Bluetooth Control
* PCA9685 Servo Driver Integration
* OLED Status Display
* Automated Pick-and-Place Operation
* Manual Jog Control
* Emergency Stop Function
* Save Current Position as Home
* Smooth Trajectory Planning
* Wrist Rotation Demonstration
* Gripper Open/Close Control
* Real-Time Position Adjustment

---

## Hardware Components

* ESP32 Development Board
* PCA9685 16-Channel PWM Servo Driver
* 5 Servo Motors
* Servo Gripper
* 128×64 SPI OLED Display
* External Servo Power Supply
* Robotic Arm Mechanical Structure

---

## OLED Connections

| OLED Pin | ESP32 Pin |
| -------- | --------- |
| VCC      | 3.3V      |
| GND      | GND       |
| CLK/SCK  | GPIO18    |
| MOSI/SDA | GPIO23    |
| DC       | GPIO13    |
| CS       | GPIO14    |
| RST      | GPIO4     |

---

## PCA9685 Servo Mapping

| Joint               | PCA9685 Channel |
| ------------------- | --------------- |
| J1 (Base Rotation)  | P0              |
| J2 (Shoulder)       | P1              |
| J3 (Elbow)          | P2              |
| J4 (Wrist Rotation) | P3              |
| J5 (Wrist Pitch)    | P4              |
| Gripper             | P5              |

---

## Predefined Positions

### Home Position

J1 = 0
J2 = 0
J3 = 0
J4 = 0
J5 = 0

### Pick Position (P1)

J1 = 80
J2 = -45
J3 = 40
J4 = 0
J5 = -30

### Drop Position (P2)

J1 = 0
J2 = -45
J3 = 40
J4 = 0
J5 = -30

---

## Bluetooth Commands

### Arm Motion

| Command | Function        |
| ------- | --------------- |
| W       | Forward Motion  |
| S       | Backward Motion |
| A       | Rotate Left     |
| D       | Rotate Right    |
| I       | Arm Up          |
| K       | Arm Down        |
| J       | Wrist Left      |
| M       | Wrist Right     |

### Gripper Control

| Command | Function               |
| ------- | ---------------------- |
| F       | Close Gripper          |
| G       | Open Gripper           |
| M0-M100 | Set Gripper Percentage |

Examples:

* M0 = Fully Open
* M50 = Half Closed
* M100 = Fully Closed

### System Commands

| Command | Function                      |
| ------- | ----------------------------- |
| V       | Save Current Position as Home |
| P       | Return to Home Position       |
| START   | Run Automatic Pick-and-Place  |
| AUTO    | Run Automatic Pick-and-Place  |
| STOP    | Emergency Stop                |
| T       | Emergency Stop                |

---

## Automatic Pick-and-Place Sequence

1. Move to Home Position
2. Open Gripper
3. Move Above Pick Location (P1)
4. Descend Vertically
5. Close Gripper and Pick Object
6. Lift Object Vertically
7. Move Toward Drop Location (P2)
8. Descend to Drop Position
9. Perform Wrist Rotation Demonstration
10. Release Object
11. Return to Home Position

The sequence is repeated three times in automatic mode.

---

## Motion Planning

The robotic arm uses a quintic smooth-step trajectory function:

* Smooth acceleration
* Constant velocity region
* Smooth deceleration

This approach significantly reduces servo jerking and improves motion quality compared to direct position jumps.

---

## OLED Interface

The OLED display provides:

* System Status
* Bluetooth Status
* Current Operation
* Pick-and-Place Progress
* Error Messages
* Emergency Stop Notifications

---

## Software Used

* PlatformIO
* Visual Studio Code
* ESP32 Arduino Framework
* Adafruit PWM Servo Driver Library
* Adafruit SSD1306 Library
* Adafruit GFX Library
* BluetoothSerial Library

---

## Applications

* Educational Robotics
* Industrial Pick-and-Place Demonstrations
* Embedded Systems Projects
* Human-Robot Interaction
* Wireless Robotic Manipulation
* Automation Training

---

## Future Improvements

* Inverse Kinematics (IK)
* Computer Vision Object Detection
* ROS2 Integration
* Mobile Application Dashboard
* Voice Command Interface
* Autonomous Object Sorting
* AI-Based Object Recognition

---

## Author

Sahil Thakur

B.Tech Electronics and Communication Engineering

Jawaharlal Nehru Government Engineering College (JNGEC)

---

## Project Demonstration

This project demonstrates a Bluetooth-enabled robotic manipulation system capable of performing smooth automated pick-and-place operations with OLED feedback, trajectory smoothing, and real-time wireless control using an ESP32-based embedded platform.
