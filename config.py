import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("APP_PORT", "5000"))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "8388608"))
    DATABASE_URL = os.getenv("DATABASE_URL", str(BASE_DIR / "instance" / "aelms.db"))
    MODEL_PATH = os.getenv("MODEL_PATH", str(BASE_DIR / "models" / "yolov8n.pt"))
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "instance" / "uploads"))
    MOCK_MODE = os.getenv("AELMS_MOCK_MODE", "true").lower() in {"1", "true", "yes", "on"}
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "mp4", "mov", "avi"}
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}
    CONGESTION_THRESHOLDS = {"low": 5, "moderate": 10, "heavy": 15}
