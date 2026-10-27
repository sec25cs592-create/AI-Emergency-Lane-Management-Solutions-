from typing import Dict


def estimate_congestion(vehicle_count: int) -> str:
    if vehicle_count >= 12:
        return "heavy"
    if vehicle_count >= 6:
        return "moderate"
    return "low"


def summarize_traffic(vehicle_count: int, emergency_detected: bool = False) -> Dict[str, object]:
    status = "priority" if emergency_detected else estimate_congestion(vehicle_count)
    message = "Emergency corridor is active." if emergency_detected else "Traffic flow is within prototype estimate ranges."
    return {
        "vehicle_count": vehicle_count,
        "status": status,
        "emergency_detected": emergency_detected,
        "message": message,
    }
