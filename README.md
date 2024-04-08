# Lancer Lumineers MATE ROV Competition Pioneer/Explorer 2023-24

# ROV Hydra Control System 

## Overview
This repository contains the code for a Remotely Operated Vehicle (ROV) control system, utilizing Pygame for the graphical user interface (GUI) and serial communication for hardware interaction. The project is designed to control an ROV through a user-friendly interface, allowing for joystick-based navigation, real-time video feedback, and customizable control widgets.

# Files Description
- `JoyStick_constants.py`: Defines the mapping of joystick buttons and axes for control commands.
- `JoyStick_test.py`: Script for testing joystick functionality and input handling.
- `ROV_main.py`: The main control script integrating joystick input, GUI updates, and hardware control commands.
- `widgets2.py`: Defines custom Pygame widgets for the GUI, including toggles, displays, and sliders.
- `Arduino_for_ROV.ino`: Arduino sketch for receiving control signals and managing hardware components like servos and sensors.

# Key Features:
Pygame GUI: A custom GUI setup that includes a main view area and a sidebar for additional controls and information.

Joystick Control: Interprets joystick inputs for ROV movement, using mathematical calculations to translate joystick position into commands.

Serial Communication: Sends commands to the ROV's Arduino controller, allowing for real-time control of the vehicle.

Live video capture: Two onboard cameras, one main and one auxillary camera capture live video of ROV's underwater environment to enable Pilot to navigate.

Image Capture: Utilizes Pygame's camera module for capturing images, which can be used for navigation or documentation. (Needs to be configured)

Future Plans:

3D Photogrammetry: With hardware and software upgrades, the ROV can perform 3D photogrammetry underwater. 

Autonomous movement: With hardware and software upgrades, the ROV can perform autopathing or predefined pathing underwater.

---

# Getting Started
To run the ROV control system, ensure you have Python installed along with the Pygame library and the PySerial module for serial communication. Clone this repository, and run ROV_final.py to start the control interface.

---

# Prerequisites
- Python 3.x
- Pygame library
- PySerial library
- Arduino IDE
- ArduinoJson library for Arduino

---
# Installation
1. Clone this repository to your local machine.
2. Ensure all prerequisites are installed.
```python
pip install pygame pyserial
```
3. Upload `Arduino_for_ROV.ino` to your Arduino board.
4. Run `ROV_main.py` to start the control system.

# Contributing
Contributions to the ROV control system are welcome. Please feel free to fork the repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

# License
This project is licensed under the MIT License - see the LICENSE file for details.
Feel free to adjust the content to match your project's specifics or personal preferences better.
