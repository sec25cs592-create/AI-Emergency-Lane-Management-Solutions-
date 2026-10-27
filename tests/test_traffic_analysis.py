from app.traffic_analysis import estimate_congestion, summarize_traffic


def test_estimate_congestion_for_low_count():
    assert estimate_congestion(2) == "low"


def test_estimate_congestion_for_high_count():
    assert estimate_congestion(9) == "moderate"
    assert estimate_congestion(12) == "heavy"


def test_summarize_traffic_uses_vehicle_count():
    summary = summarize_traffic(5, emergency_detected=False)
    assert summary["vehicle_count"] == 5
    assert summary["status"] in {"low", "moderate", "heavy"}
