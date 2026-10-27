import io


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert "mode" in data


def test_invalid_upload_rejected(client):
    response = client.post(
        "/api/analyze",
        data={"file": (io.BytesIO(b"not an image"), "note.txt")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_reset_endpoint(client):
    response = client.post("/api/reset")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "reset"


def test_traffic_signal_simulation(client):
    response = client.post("/api/traffic/simulate", json={"signal_state": "GREEN"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["traffic"]["signal_state"] == "GREEN"


def test_event_history_endpoint_after_upload(client):
    response = client.post(
        "/api/analyze",
        data={"file": (io.BytesIO(b"fakeimagecontent"), "sample.jpg")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    events = client.get("/api/events")
    assert events.status_code == 200
    payload = events.get_json()
    assert len(payload["events"]) >= 1
