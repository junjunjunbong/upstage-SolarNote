import os
from dotenv import load_dotenv

load_dotenv()

UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
UPSTAGE_BASE_URL = "https://api.upstage.ai/v1"

SOLAR_MODEL = "solar-pro"
REQUEST_TIMEOUT = 60.0
DOCUMENT_PARSE_TIMEOUT = 120.0

MAX_RETRIES = 2

# ========== SolarNote 브랜딩 ==========
APP_NAME = "SolarNote"
APP_ICON = "☀️"
APP_TAGLINE = "태양처럼 밝게, 실수도 빛나는 배움으로"
APP_SUBTITLE = "AI 수학 오답노트"

# 색상 테마
SOLAR_PRIMARY = "#FF6B35"
SOLAR_GOLD = "#FFB347"
