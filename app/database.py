import os
import sqlite3
from typing import Any, Dict, List, Optional

_SHARED_MEMORY_CONNECTIONS: Dict[str, sqlite3.Connection] = {}


def _database_path(db_url: Optional[str] = None) -> str:
    url = db_url or os.getenv("DATABASE_URL", "./instance/aelms.db")
    return url


def get_connection(db_url: Optional[str] = None) -> sqlite3.Connection:
    url = _database_path(db_url)

    if url == ":memory:":
        if url not in _SHARED_MEMORY_CONNECTIONS:
            connection = sqlite3.connect(":memory:")
            connection.row_factory = sqlite3.Row
            _SHARED_MEMORY_CONNECTIONS[url] = connection
        return _SHARED_MEMORY_CONNECTIONS[url]

    directory = os.path.dirname(url)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    connection = sqlite3.connect(url)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(db_url: Optional[str] = None) -> None:
    connection = get_connection(db_url)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS detection_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            detected_class TEXT NOT NULL,
            confidence REAL NOT NULL,
            source_type TEXT NOT NULL,
            emergency_alert INTEGER NOT NULL,
            simulated_signal TEXT NOT NULL
        )
        """
    )
    connection.commit()


def log_detection_event(
    detected_class: str,
    confidence: float,
    source_type: str,
    emergency_alert: bool,
    simulated_signal: str,
    db_url: Optional[str] = None,
) -> Dict[str, Any]:
    from datetime import datetime, timezone

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    connection = get_connection(db_url)
    cursor = connection.execute(
        """
        INSERT INTO detection_events (
            timestamp, detected_class, confidence, source_type, emergency_alert, simulated_signal
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        (timestamp, detected_class, confidence, source_type, int(emergency_alert), simulated_signal),
    )
    connection.commit()
    record_id = cursor.lastrowid

    return {
        "id": record_id,
        "timestamp": timestamp,
        "detected_class": detected_class,
        "confidence": confidence,
        "source_type": source_type,
        "emergency_alert": emergency_alert,
        "simulated_signal": simulated_signal,
    }


def get_recent_events(limit: int = 20, db_url: Optional[str] = None) -> List[Dict[str, Any]]:
    connection = get_connection(db_url)
    rows = connection.execute(
        "SELECT * FROM detection_events ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [dict(row) for row in rows]


def clear_events(db_url: Optional[str] = None) -> None:
    connection = get_connection(db_url)
    connection.execute("DELETE FROM detection_events")
    connection.commit()
