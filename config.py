import os
from dotenv import load_dotenv

load_dotenv()

UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
UPSTAGE_BASE_URL = "https://api.upstage.ai/v1"

SOLAR_MODEL = "solar-pro3"
REQUEST_TIMEOUT = 60.0
DOCUMENT_PARSE_TIMEOUT = 120.0

MAX_RETRIES = 2

# ========== Solar Pro 3 파라미터 설정 ==========
# 공식 문서: https://console.upstage.ai/docs
# 각 작업별 최적화된 파라미터
GENERATION_PARAMS = {
    "concept": {
        "temperature": 0.3,
        "max_tokens": 1024,
        "top_p": 0.9
    },  # 개념 분류: 낮은 temperature로 일관성 확보
    "problem": {
        "temperature": 0.8,
        "max_tokens": 4096,
        "top_p": 0.95
    },  # 문제 생성: 높은 temperature로 다양성 확보
    "solution": {
        "temperature": 0.2,
        "max_tokens": 4096,
        "top_p": 0.9
    },  # 풀이: 낮은 temperature로 정확성 확보
    "note": {
        "temperature": 0.5,
        "max_tokens": 2048,
        "top_p": 0.92
    },  # 오답노트: 중간 temperature
}

# ========== SolarNote 브랜딩 ==========
APP_NAME = "SolarNote"
APP_ICON = "☀️"
APP_TAGLINE = "태양처럼 밝게, 실수도 빛나는 배움으로"
APP_SUBTITLE = "AI 수학 오답노트"

# 색상 테마
SOLAR_PRIMARY = "#FF6B35"
SOLAR_GOLD = "#FFB347"
