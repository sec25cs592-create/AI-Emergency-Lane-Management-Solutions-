#!/usr/bin/env python3
"""Download and configure a YOLO weights file when a model is needed.

This is optional for demonstration mode. The project is designed to run without
pretrained weights by falling back to deterministic mock detection results.
"""

from __future__ import annotations

import os
from pathlib import Path


def main() -> None:
    target_dir = Path(__file__).resolve().parents[1] / "models"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / "yolov8n.pt"

    print(f"Model download target: {target_path}")
    print("This example documents where a YOLO weights file can be placed.")
    print("For a real deployment, download a supported model from Ultralytics and set MODEL_PATH in the environment.")
    print("The app can still run in mock mode without a downloaded model.")

    if not target_path.exists():
        print("No weights file was downloaded in this demo run.")
    else:
        print(f"Weights file already present: {target_path}")


if __name__ == "__main__":
    main()
