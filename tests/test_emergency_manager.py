from app.emergency_manager import EmergencyManager


def test_emergency_manager_detects_ambulance():
    manager = EmergencyManager()
    alert = manager.evaluate([{"class_name": "ambulance", "confidence": 0.95}])
    assert alert["emergency_detected"] is True
    assert alert["signal_state"] == "GREEN"


def test_emergency_manager_invalid_signal_rejected():
    manager = EmergencyManager()
    result = manager.apply_manual_override("PURPLE")
    assert result["status"] == "error"
    assert "invalid" in result["message"].lower()
