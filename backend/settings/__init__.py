import os

from dotenv import load_dotenv


load_dotenv()

DB_URI = os.getenv("DB_URI", "sqlite+aiosqlite:///./ai_naming.db")
DB_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.qq.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
MAIL_FROM = os.getenv("MAIL_FROM", MAIL_USERNAME)
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "AI 起名")
MAIL_STARTTLS = os.getenv("MAIL_STARTTLS", "true").lower() == "true"
MAIL_SSL_TLS = os.getenv("MAIL_SSL_TLS", "false").lower() == "true"
USE_CREDENTIALS = os.getenv("USE_CREDENTIALS", "true").lower() == "true"

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-production")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
