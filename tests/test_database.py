from app.database import get_recent_events, init_db, log_detection_event


def test_database_event_is_created_and_retrieved():
    db_url = ":memory:"
    init_db(db_url)
    event = log_detection_event(
        detected_class="ambulance",
        confidence=0.98,
        source_type="upload",
        emergency_alert=True,
        simulated_signal="GREEN",
        db_url=db_url,
    )

    assert event["detected_class"] == "ambulance"
    rows = get_recent_events(limit=10, db_url=db_url)
    assert len(rows) >= 1
    assert rows[0]["simulated_signal"] == "GREEN"
