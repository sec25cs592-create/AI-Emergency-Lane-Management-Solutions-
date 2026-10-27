# Third-Party Notices

This project uses open-source libraries and optional model tooling. Some third-party packages are not covered by this project's MIT license and may carry their own terms.

## Included Dependencies

### Flask
- License: BSD-3-Clause
- Project: https://flask.palletsprojects.com/
- Purpose: Backend web framework for the API and dashboard.

### OpenCV (opencv-python-headless)
- License: Apache 2.0 and BSD-style licensing terms depending on components
- Project: https://opencv.org/
- Purpose: Image and video processing utilities.

### python-dotenv
- License: BSD-3-Clause
- Project: https://github.com/theskumar/python-dotenv
- Purpose: Load environment variables from `.env` files.

### Pytest
- License: MIT
- Project: https://pytest.org/
- Purpose: Automated testing.

### Werkzeug
- License: BSD-3-Clause
- Project: https://werkzeug.palletsprojects.com/
- Purpose: WSGI utilities used by Flask.

## Optional Model Dependency

Ultralytics is optional and is not required for the default mock mode.

- License: AGPL-3.0 or proprietary commercial terms depending on usage and deployment context; verify the exact license for your environment before production use.
- Project: https://github.com/ultralytics/ultralytics
- Purpose: YOLO object detection model integration.

Important: This project does not include or redistribute any pretrained YOLO weights unless expressly downloaded by the user in their own environment. The repository does not claim that any external model file is covered under the project's MIT License.

## Sample Data and Media

The sample detection and traffic scenario files in `sample_data/` are illustrative synthetic examples for testing and demonstration. They are not sourced from official traffic datasets and are not claimed to be real-world measured traffic data.

## License Notice

The project source code in this repository is licensed under the MIT License in [LICENSE](LICENSE). Third-party packages retain their own copyright and licensing terms. Please review each dependency's license before using this project in a commercial or public deployment scenario.
