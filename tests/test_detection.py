from app.detection import DetectionEngine


def test_mock_detection_returns_expected_shape():
    engine = DetectionEngine(mock_mode=True)
    result = engine.detect_from_path("sample.jpg")
    assert "detections" in result
    assert "emergency_detected" in result
    assert isinstance(result["detections"], list)


def test_detection_rejects_unsupported_format():
    engine = DetectionEngine(mock_mode=True)
    result = engine.detect_from_path("sample.txt")
    assert result["status"] == "error"
    assert "unsupported" in result["message"].lower()
