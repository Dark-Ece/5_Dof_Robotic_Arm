# LiDAR-Based 5DOF Robotic Arm with Bluetooth Control

## Overview

This project is a 5 Degrees of Freedom (5DOF) robotic arm controlled using an ESP32 microcontroller, PCA9685 servo driver, and Bluetooth communication. The robotic arm is capable of performing automated pick-and-place operations as well as manual position control through a mobile application.

The system demonstrates smooth robotic motion using interpolation-based trajectory planning, predefined motion sequences, and wireless control through Bluetooth.

---

## Features

- 5DOF Robotic Arm
- ESP32 Bluetooth Control
- PCA9685 Servo Driver Integration
- Smooth Motion Planning
- Automated Pick and Place Operation
- Wireless Smartphone Control
- Preset Position Commands
- Servo Gripper Control
- OLED Status Display
- Real-Time Position Control

---

## Hardware Components

- ESP32 Development Board
- PCA9685 16-Channel Servo Driver
- 5 Servo Motors
- Servo Gripper
- 128×64 SPI OLED Display
- External Power Supply
- Robotic Arm Structure

---

## OLED Connections

| OLED Pin | ESP32 Pin |
|-----------|-----------|
| VCC | 3.3V |
| GND | GND |
| CLK/SCK | GPIO18 |
| SDA/MOSI | GPIO23 |
| DC | GPIO13 |
| CS | GPIO14 |
| RST | GPIO4 |

---

## PCA9685 Servo Mapping

| Joint | PCA9685 Channel |
|---------|---------|
| J1 (Base Rotation) | P0 |
| J2 (Shoulder) | P1 |
| J3 (Elbow) | P2 |
| J4 (Wrist Rotation) | P3 |
| J5 (Wrist Pitch) | P4 |
| Gripper | P5 |

---

## Robotic Arm Positions

### Home Position

0, 0, 0, 0, 0

### Pick Position (P1)

80, -45, 40, 0, -30

### Drop Position (P2)

0, -45, 40, 0, -30

---

## Bluetooth Commands

| Command | Function |
|----------|----------|
| A | Home Position |
| B | Ready Position |
| C | Move to Pick Position (P1) |
| D | Close Gripper |
| E | Lift Object |
| F | Move to Drop Position (P2) |
| G | Open Gripper |
| H | Automatic Pick-and-Place Cycle |

---

## Working Principle

1. Robotic arm initializes in the Home Position.
2. Arm moves above the target object.
3. End-effector descends vertically from the top.
4. Gripper closes and grasps the object.
5. Arm lifts the object vertically.
6. Arm moves toward the drop location.
7. Wrist performs a small rotation for realistic placement.
8. Gripper releases the object.
9. Arm returns to Home Position.
10. Process repeats automatically.

---

## Software Used

- PlatformIO
- Visual Studio Code
- ESP32 Arduino Framework
- Adafruit PWM Servo Driver Library
- BluetoothSerial Library

---

## Applications

- Industrial Pick and Place
- Educational Robotics
- Embedded Systems Learning
- Automation Demonstration
- Smart Manufacturing Concepts
- Wireless Robotic Control

---

## Future Improvements

- Inverse Kinematics (IK)
- Computer Vision Object Detection
- ROS2 Integration
- Mobile Application Interface
- Voice-Controlled Operation
- Autonomous Object Sorting
- AI-Based Object Recognition

---

## Author

**Sahil Thakur**

B.Tech Electronics and Communication Engineering

Jawaharlal Nehru Government Engineering College (JNGEC)

---

## Project Demonstration

This project demonstrates smooth robotic manipulation, wireless Bluetooth control, automated pick-and-place operations, and embedded control techniques using ESP32 and PCA9685 servo driver technology.
