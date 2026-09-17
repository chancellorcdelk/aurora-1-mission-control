# AURORA-1 Mission Control

A browser-based spacecraft command and telemetry simulator built with Python and Flask.

## Overview

AURORA-1 Mission Control simulates a spacecraft operations dashboard with live telemetry, subsystem health monitoring, fault detection, operator controls, telemetry history, and mission event logging.

## Features

- Simulated spacecraft telemetry
  - Battery level
  - Temperature
  - Altitude
  - Mission mode
  - Overall system status

- Automated fault detection
  - Low battery warnings
  - Thermal warnings
  - EPS, ADCS, COMMS, and OBC subsystem monitoring

- Mission control commands
  - Science Mode
  - Communication Mode
  - Standby Mode

- Mission event logging

- Battery condition visualization

- Live telemetry history graphs

- Mission elapsed time

## Technologies

- Python
- Flask
- HTML
- CSS
- JavaScript
- Jinja2
- Chart.js

## Project Structure

```text
mission-control-web-app/
├── app.py
├── requirements.txt
├── static/
│   └── style.css
└── templates/
    └── index.html