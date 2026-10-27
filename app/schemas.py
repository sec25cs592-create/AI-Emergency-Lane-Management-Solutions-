from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class DetectionRecord:
    class_name: str
    confidence: float
    x1: int = 0
    y1: int = 0
    x2: int = 0
    y2: int = 0
    timestamp: str = ""
    source_type: str = "upload"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "class_name": self.class_name,
            "confidence": self.confidence,
            "bbox": [self.x1, self.y1, self.x2, self.y2],
            "timestamp": self.timestamp,
            "source_type": self.source_type,
        }


@dataclass
class TrafficSnapshot:
    vehicle_count: int = 0
    status: str = "low"
    emergency_detected: bool = False
    signal_state: str = "RED"
    message: str = "System ready."
    history: List[Dict[str, Any]] = field(default_factory=list)
