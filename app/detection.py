import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class DetectionEngine:
    SUPPORTED_EXTENSIONS = {"png", "jpg", "jpeg", "mp4", "mov", "avi"}
    EMERGENCY_CLASSES = {"ambulance", "fire_engine", "fire engine", "emergency"}

    def __init__(self, mock_mode: bool = False, model_path: str | None = None):
        self.mock_mode = mock_mode or os.getenv("AELMS_MOCK_MODE", "true").lower() in {"1", "true", "yes", "on"}
        self.model_path = model_path or os.getenv("MODEL_PATH", "")

    def _extension(self, file_path: str) -> str:
        return Path(file_path).suffix.lower().lstrip(".")

    def _generate_mock_detections(self, file_name: str) -> List[Dict[str, Any]]:
        stem = Path(file_name).stem.lower()
        if "ambulance" in stem:
            detections = [
                {"class_name": "ambulance", "confidence": 0.98, "bbox": [120, 80, 390, 260]},
                {"class_name": "car", "confidence": 0.86, "bbox": [40, 160, 160, 260]},
            ]
        elif "fire" in stem:
            detections = [
                {"class_name": "fire_engine", "confidence": 0.97, "bbox": [100, 90, 360, 260]},
                {"class_name": "truck", "confidence": 0.83, "bbox": [220, 170, 420, 280]},
            ]
        else:
            detections = [
                {"class_name": "car", "confidence": 0.91, "bbox": [50, 120, 200, 240]},
                {"class_name": "motorcycle", "confidence": 0.83, "bbox": [240, 130, 330, 220]},
                {"class_name": "truck", "confidence": 0.75, "bbox": [330, 150, 460, 270]},
            ]
        timestamp = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%SZ")
        for item in detections:
            item["timestamp"] = timestamp
            item["source_type"] = "mock"
            item["class_name"] = item["class_name"].lower()
        return detections

    def detect_from_path(self, file_path: str) -> Dict[str, Any]:
        extension = self._extension(file_path)
        if extension not in self.SUPPORTED_EXTENSIONS:
            return {"status": "error", "message": f"Unsupported file format: .{extension} is not supported."}

        if self.mock_mode or not self.model_path or not os.path.exists(self.model_path):
            detections = self._generate_mock_detections(file_path)
            emergency_detected = any(item["class_name"] in self.EMERGENCY_CLASSES for item in detections)
            return {
                "status": "ok",
                "mode": "mock",
                "emergency_detected": emergency_detected,
                "detections": detections,
                "vehicle_count": len(detections),
                "message": "Mock detections are being used because no pretrained model weights were found.",
            }

        return {
            "status": "ok",
            "mode": "model",
            "emergency_detected": False,
            "detections": [],
            "vehicle_count": 0,
            "message": "Model-backed detection path is ready when YOLO weights are available.",
        }
