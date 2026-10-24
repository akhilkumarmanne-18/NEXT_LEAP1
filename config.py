import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'nextleap-default-secret-key-2026')
    
    # Database config: prefer DATABASE_URL, fallback to SQLite
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        sqlite_path = BASE_DIR / 'database' / 'nextleap.db'
        database_url = f"sqlite:///{sqlite_path.as_posix()}"
    
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security & session
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    
    # AI Engine Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'auto')
