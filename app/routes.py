import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from flask import Flask, jsonify, request, render_template
from werkzeug.utils import secure_filename

from app.database import clear_events, get_recent_events, log_detection_event
from app.detection import DetectionEngine
from app.emergency_manager import EmergencyManager
from app.traffic_analysis import summarize_traffic
from config import Config


def _allowed_file(filename: str, allowed_exts: set[str]) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_exts


def register_routes(app: Flask) -> None:
    app.config.setdefault("TRAFFIC_STATE", {
        "vehicle_count": 0,
        "status": "low",
        "emergency_detected": False,
        "signal_state": "RED",
        "message": "System ready.",
    })
    app.config.setdefault("EMERGENCY_MANAGER", EmergencyManager())
    app.config.setdefault("DETECTION_ENGINE", DetectionEngine(mock_mode=app.config.get("MOCK_MODE", True)))

    os.makedirs(app.config.get("UPLOAD_FOLDER", Config.UPLOAD_FOLDER), exist_ok=True)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/health")
    def health():
        return jsonify({
            "status": "ok",
            "mode": "mock" if app.config["MOCK_MODE"] else "model",
            "model_available": not app.config["MOCK_MODE"],
            "message": "Prototype is running in mock mode without pretrained weights.",
        })

    @app.route("/api/events")
    def events():
        return jsonify({"events": get_recent_events(limit=25, db_url=app.config["DATABASE_URL"])})

    @app.route("/api/analyze", methods=["POST"])
    def analyze():
        file = request.files.get("file")
        if file is None or file.filename == "":
            return jsonify({"error": "No file uploaded."}), 400

        if not _allowed_file(file.filename, app.config["ALLOWED_EXTENSIONS"]):
            return jsonify({"error": "Unsupported file format. Allowed: PNG, JPG, JPEG, MP4, MOV, AVI."}), 400

        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        if size > app.config["MAX_CONTENT_LENGTH"]:
            return jsonify({"error": "File exceeds size limit."}), 413

        upload_dir = Path(app.config.get("UPLOAD_FOLDER", Config.UPLOAD_FOLDER))
        upload_dir.mkdir(parents=True, exist_ok=True)
        safe_name = secure_filename(file.filename)
        temp_path = upload_dir / safe_name
        file.save(temp_path)

        engine = app.config["DETECTION_ENGINE"]
        results = engine.detect_from_path(str(temp_path))

        if results.get("status") == "error":
            return jsonify({"error": results.get("message", "Analysis failed.")}), 400

        emergency_alert = bool(results.get("emergency_detected"))
        manager = app.config["EMERGENCY_MANAGER"]
        alert = manager.evaluate(results.get("detections", []))
        vehicle_count = len(results.get("detections", []))
        summary = summarize_traffic(vehicle_count, emergency_alert)
        app.config["TRAFFIC_STATE"] = {
            "vehicle_count": vehicle_count,
            "status": summary["status"],
            "emergency_detected": emergency_alert,
            "signal_state": alert["signal_state"],
            "message": alert["message"],
        }

        for detection in results.get("detections", []):
            log_detection_event(
                detected_class=detection.get("class_name", "unknown"),
                confidence=float(detection.get("confidence", 0.0)),
                source_type="upload",
                emergency_alert=emergency_alert,
                simulated_signal=alert["signal_state"],
                db_url=app.config["DATABASE_URL"],
            )

        return jsonify({
            "status": "ok",
            "detection": results,
            "traffic": app.config["TRAFFIC_STATE"],
            "alert": alert,
        })

    @app.route("/api/traffic/status")
    def traffic_status():
        return jsonify({"traffic": app.config["TRAFFIC_STATE"]})

    @app.route("/api/traffic/simulate", methods=["POST"])
    def traffic_simulate():
        payload = request.get_json(silent=True) or {}
        signal_state = payload.get("signal_state") or payload.get("state")
        if signal_state is None:
            return jsonify({"error": "Request body must include a traffic light state."}), 400

        manager = app.config["EMERGENCY_MANAGER"]
        result = manager.apply_manual_override(str(signal_state))
        if result.get("status") == "error":
            return jsonify(result), 400

        app.config["TRAFFIC_STATE"]["signal_state"] = result["signal_state"]
        app.config["TRAFFIC_STATE"]["message"] = result["message"]
        return jsonify({"status": "ok", "traffic": app.config["TRAFFIC_STATE"], "signal": result})

    @app.route("/api/reset", methods=["POST"])
    def reset_state():
        manager = app.config["EMERGENCY_MANAGER"]
        result = manager.reset()
        app.config["TRAFFIC_STATE"] = {
            "vehicle_count": 0,
            "status": "low",
            "emergency_detected": False,
            "signal_state": result["signal_state"],
            "message": result["message"],
        }
        clear_events(app.config["DATABASE_URL"])
        return jsonify({"status": "reset", "traffic": app.config["TRAFFIC_STATE"], "signal": result})
