# AELMS — AI Emergency Lane Management System

AELMS is a college-level prototype for AI-powered emergency traffic management. It demonstrates how a camera-based system can detect emergency vehicles, estimate traffic congestion, and simulate an emergency corridor so an ambulance or fire engine could be prioritized at a junction.

This repository is intentionally designed to run on a normal Windows PC without physical hardware. It supports a mock detection mode when pretrained model weights are unavailable, and it includes optional documentation for future ESP32-style hardware integration.

## Problem Statement

Emergency vehicles often face delays when traffic is dense or when signal control is not optimized for priority movement. Delays in emergency response can increase risk to patients and communities. A low-cost prototype that uses camera-based detection and simulated signal prioritization can help students and researchers demonstrate how such a system could work in a smart-city context.

## Project Objectives

- Detect emergency vehicles such as ambulances and fire engines using image and video analysis.
- Estimate traffic congestion from camera-based vehicle counts.
- Trigger a simulated emergency corridor signal when an emergency vehicle is detected.
- Log detection events for review and analysis.
- Provide a simple web dashboard for demo and evaluation.
- Keep the prototype runnable without a GPU or real hardware.

## Main Features

- AI detection interface with mock fallback mode
- Upload support for images and videos
- Simple webcam demo mode (simulated, not a real camera stream)
- Vehicle counting and congestion estimation
- Emergency alert logic and simulated traffic light states
- SQLite event storage for detection records
- Flask REST API for health, analysis, traffic, and event endpoints
- Responsive dark dashboard with smart-city styling
- Optional hardware integration notes for ESP32-based experiments

## Technology Stack

- Python 3.11+
- Flask
- OpenCV
- Ultralytics YOLO (optional, for real model-based inference)
- SQLite
- HTML, CSS, JavaScript
- Pytest
- Git and GitHub

## System Requirements

- Windows 10 or Windows 11
- Python 3.11 or newer
- Internet access only for optional dependency installation or model download
- A browser such as Chrome or Edge
- No specialized hardware required to run the prototype

## Installation on Windows

1. Clone the repository.
2. Open PowerShell in the project root.
3. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies.

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Environment Variables

The project uses a `.env` file for local configuration. A sample file is included at `.env.example`.

Create a `.env` file in the project root based on `.env.example`:

```env
SECRET_KEY=change-me-in-production
AELMS_MOCK_MODE=true
MODEL_PATH=./models/yolov8n.pt
DATABASE_URL=./instance/aelms.db
MAX_CONTENT_LENGTH=8388608
UPLOAD_FOLDER=./instance/uploads
APP_PORT=5000
HOST=0.0.0.0
```

Important:
- `.env` is intentionally ignored by Git.
- A real YOLO model is optional.
- The app runs in mock mode if the model is missing or the mock flag is enabled.

## AI Model Setup

This prototype is designed to work without pretrained weights. The default behavior is to run in deterministic mock mode.

If you want to use a YOLO model on a real deployment, install a compatible Ultralytics package in a Python 3.11 environment and point `MODEL_PATH` to a valid `.pt` file.

Example pattern:

```powershell
python -m pip install ultralytics==8.4.0
```

Then make sure the environment variable points to a valid file, such as:

```env
MODEL_PATH=./models/yolov8n.pt
```

If the model file is absent, the application will continue in `mock` mode and display a clear status message.

## Running the Application

From the project root:

```powershell
python app.py
```

Then open:

- http://localhost:5000/

## Running in Mock / Demo Mode

The project is already configured to run in mock mode by default. To force mock mode, set:

```env
AELMS_MOCK_MODE=true
```

You can also run the app without a model file present and the app will fall back to mock detections automatically.

## Running Tests

Use pytest from the project root:

```powershell
python -m pytest -q
```

The test suite includes:
- startup and health checks
- valid and invalid API requests
- traffic analysis logic
- emergency alert logic
- simulated signal state transitions
- database event logging
- mock detection for missing model weight scenarios
- malformed upload handling

## API Endpoints

### `GET /api/health`
Returns the app status and current operating mode.

Example response:

```json
{
  "status": "ok",
  "mode": "mock",
  "model_available": false,
  "message": "Prototype is running in mock mode without pretrained weights."
}
```

### `GET /api/events`
Returns recent detection events from SQLite.

### `POST /api/analyze`
Uploads an image or video for analysis.

Request format: multipart form data with a file named `file`.

### `GET /api/traffic/status`
Returns current vehicle count, congestion estimate, and signal state.

### `POST /api/traffic/simulate`
Applies a simulated traffic-light state change.

Example body:

```json
{
  "signal_state": "GREEN"
}
```

### `POST /api/reset`
Resets the simulation and clears event log data.

## Project Directory Structure

```text
AELMS/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── LICENSE
├── THIRD_PARTY_NOTICES.md
├── pytest.ini
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── detection.py
│   ├── traffic_analysis.py
│   ├── emergency_manager.py
│   ├── database.py
│   └── schemas.py
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── dashboard.js
├── docs/
│   ├── TECHNICAL_DESIGN.md
├── sample_data/
│   ├── README.md
│   ├── detections.json
│   └── traffic_scenarios.json
├── tests/
│   ├── conftest.py
│   ├── test_app.py
│   ├── test_detection.py
│   ├── test_traffic_analysis.py
│   ├── test_emergency_manager.py
│   └── test_database.py
├── scripts/
│   └── download_model.py
├── hardware/
│   ├── README.md
│   └── esp32_example.ino
└── instance/
```

## Screenshots

Screenshots are not included yet because this is a prototype repository. The dashboard is designed to be easy to run locally and can be captured once the app is started.

Suggested placeholders:
- Dashboard overview screenshot
- Emergency alert screenshot
- Sample upload result screenshot

## Known Limitations

- This is a prototype and not industrial-grade traffic control software.
- The emergency detection is based on a mock detection mode or optional model integration.
- Traffic congestion values are estimates derived from camera data, not official traffic measurement devices.
- Real signal control is intentionally not connected to public infrastructure by default.
- Live camera access depends on local hardware availability and browser permissions.

## Troubleshooting

### Issue: `pytest` not found
Use the project virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest -q
```

### Issue: no model is found
The app will fall back to mock mode automatically. Verify that `AELMS_MOCK_MODE=true` is set or the model file path is absent.

### Issue: upload rejected
Check that the uploaded file extension is one of: `.png`, `.jpg`, `.jpeg`, `.mp4`, `.mov`, or `.avi`.

### Issue: database not found
Ensure the `instance` directory exists or the database path is valid and writable.

## Future Enhancements

- Real-time camera stream processing
- Better emergency vehicle model training and validation
- Traffic density analytics using time-series data
- Live edge deployment on a Raspberry Pi or Jetson device
- Integration with a real traffic signal controller in a controlled test environment
- Secure multi-user management and audit logs

## Contribution Guidelines

Contributions are welcome if they improve the prototype and keep the project academically sound.

1. Fork the repository.
2. Create a feature branch.
3. Add or update tests for your change.
4. Run the relevant pytest checks.
5. Submit a clear pull request with explanation and screenshots if relevant.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for full terms.

## Implemented vs Simulated Features

Implemented features:
- backend API
- mock detection engine
- traffic congestion logic
- emergency alert logic
- SQLite event logging
- dashboard UI
- tests

Simulated or optional features:
- real YOLO model inference
- webcam hardware integration
- actual traffic light control hardware
- public traffic infrastructure integration

> This prototype clearly labels all traffic control behavior as simulated. It is not authorized to manage real public traffic systems unless separately approved and validated in a real test environment.
