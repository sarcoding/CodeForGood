# TrafficGuardian

Traffic System 


![Recording 2023-09-10 223932](https://github.com/sarcoding/TrafficGuardian/assets/92933416/d3455067-2a06-4ec7-bda0-814b5907222e)

# TrafficGuardian: Traffic Management and Vehicle Tracking

TrafficGuardian is a comprehensive traffic management system that combines real-time vehicle tracking, traffic signal management, and signal violation detection. This system helps optimize traffic flow, reduce congestion, and enhance road safety.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Demo](#demo)
- [Acknowledgments](#acknowledgments)

## Overview

TrafficGuardian is designed to streamline traffic management in urban areas by harnessing the power of modern computer vision and artificial intelligence. It provides a range of features aimed at improving traffic flow, monitoring vehicle movements, and ensuring road safety.

## Features

- *Vehicle Tracking*: Utilizes YOLO (You Only Look Once) for real-time vehicle object tracking.
- *Vehicle Counting*: Counts the number of vehicles in specified regions to determine traffic density.
- *Traffic Signal Management*: Adjusts signal timings based on vehicle count to optimize traffic flow.
- *Signal Violation Detection*: Detects vehicles attempting to cross a red signal, enhancing safety.

## Installation

1. Clone the repository:

   bash
   git clone https://github.com/your-username/trafficguardian.git

2. Install the required libraries

   bash
   pip install -r requirements.txt

## Usage

1. Run the launch.py file, for object counting and tracking

   bash
   python launch.py

2. Run the central_hub.py file, for managing the signal timing based on the real-time data recieved from launch.py

   bash
   python central_hub.py 
