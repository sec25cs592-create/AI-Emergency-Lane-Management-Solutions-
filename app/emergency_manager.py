from typing import Dict, Iterable, List, Optional


class EmergencyManager:
    VALID_SIGNAL_STATES = {"RED", "YELLOW", "GREEN"}
    EMERGENCY_CLASSES = {"ambulance", "fire_engine", "fire engine", "emergency"}

    def __init__(self):
        self.signal_state = "RED"
        self.emergency_detected = False

    def evaluate(self, detections: Iterable[Dict[str, object]]) -> Dict[str, object]:
        detection_list = list(detections or [])
        matches = [
            item.get("class_name", "").lower()
            for item in detection_list
            if isinstance(item, dict)
        ]
        self.emergency_detected = any(item in self.EMERGENCY_CLASSES for item in matches)

        if self.emergency_detected:
            self.signal_state = "GREEN"
            return {
                "emergency_detected": True,
                "signal_state": self.signal_state,
                "message": "Emergency vehicle detected. Simulated signal is set to green for priority passage.",
            }

        return {
            "emergency_detected": False,
            "signal_state": self.signal_state,
            "message": "No emergency vehicle detected. Normal traffic simulation continues.",
        }

    def apply_manual_override(self, signal_state: str) -> Dict[str, object]:
        normalized = str(signal_state or "").upper()
        if normalized not in self.VALID_SIGNAL_STATES:
            return {"status": "error", "message": f"Invalid signal state '{signal_state}'. Allowed values are RED, YELLOW, GREEN."}

        self.signal_state = normalized
        return {"status": "ok", "signal_state": self.signal_state, "message": f"Manual override set to {self.signal_state}."}

    def reset(self) -> Dict[str, object]:
        self.signal_state = "RED"
        self.emergency_detected = False
        return {"status": "reset", "signal_state": self.signal_state, "message": "Simulation reset to default state."}
