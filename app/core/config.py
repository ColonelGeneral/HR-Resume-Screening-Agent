from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
LOG_DIR = ROOT_DIR / "logs"
DOCS_DIR = ROOT_DIR / "docs"
DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)


@dataclass(frozen=True)
class Settings:
    app_name: str = "HR Resume & LinkedIn Shortlisting Agent"
    environment: str = os.getenv("ENVIRONMENT", "development")
    database_url: str = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'hr_shortlisting.db'}")
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    api_key: str | None = os.getenv("API_KEY")
    jwt_secret: str = os.getenv("JWT_SECRET", "change-me")
    ocr_enabled: bool = os.getenv("OCR_ENABLED", "true").lower() in {"1", "true", "yes"}
    max_upload_mb: int = int(os.getenv("MAX_UPLOAD_MB", "10"))
    allowed_extensions: tuple[str, ...] = (".pdf", ".docx", ".txt", ".json")
    max_input_chars: int = int(os.getenv("MAX_INPUT_CHARS", "50000"))
    confidence_threshold: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.65"))


settings = Settings()
