# Sample Data

This directory contains sample records and traffic scenarios used for demonstrations, testing, and developer validation.

## Included Files

- `detections.json`: Example detected objects and event records with timestamps, confidence scores, and source labels.
- `traffic_scenarios.json`: Example conditions for normal flow, congestion, ambulance detection, fire engine detection, and no-emergency traffic states.

## Usage

These files are not used as training data. They are demonstration artifacts only. They are intended to show realistic formats for the prototype and help validate application logic without requiring a GPU or external model downloads.

## Notes

- All examples are illustrative and must be treated as mock data for academic testing purposes.
- Confidence scores and counts are not claimed to represent field-grade measurements.
- Use the mock mode or test fixtures for local reproducible runs.
