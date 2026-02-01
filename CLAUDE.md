# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

SolarNote는 수학 문제 이미지를 분석하여 오답 노트를 자동 생성하는 AI 애플리케이션입니다. Streamlit 프론트엔드와 Upstage API(Solar Pro 3, Document Parse, Information Extract)를 사용합니다.

## 명령어

```bash
# 의존성 설치
pip install -r requirements.txt

# 애플리케이션 실행
streamlit run app.py
```

## 환경 설정

`.env` 파일에 Upstage API 키 필요:
```
UPSTAGE_API_KEY=your_api_key_here
```

## 아키텍처

### Multi-Agent 파이프라인

```
이미지 업로드 → OrchestratorAgent (전체 워크플로우 조율)
    ├── ParserAgent      → Document Parse API (OCR + 차트 인식)
    ├── ExtractorAgent   → Information Extract API (필드 추출)
    ├── ConceptAgent     → Solar Pro 3 (주제/난이도 분류)
    ├── ProblemAgent     → Solar Pro 3 (유사 문제 5개 생성)
    ├── SolutionAgent    → Solar Pro 3 (풀이 작성)
    └── NoteAgent        → Solar Pro 3 (오답 노트 생성)
    → 최종 오답 노트 출력
```

### 폴더 구조

- `agents/` - 6개의 특화된 에이전트 클래스 (BaseAgent 상속)
- `core/upstage_client.py` - Upstage API 래퍼 (최신 파라미터 지원)
- `models/schemas.py` - 7개의 dataclass 스키마
- `prompts/templates.py` - LLM 프롬프트 + System Prompts
- `ui/` - Streamlit UI 컴포넌트 및 CSS 스타일링

### 주요 설정값 (config.py)

```python
SOLAR_MODEL = "solar-pro3"  # 최신 MoE 모델
REQUEST_TIMEOUT = 60.0
DOCUMENT_PARSE_TIMEOUT = 120.0
MAX_RETRIES = 2

# 작업별 최적화된 파라미터
GENERATION_PARAMS = {
    "concept":    {"temperature": 0.3, "max_tokens": 1024, "top_p": 0.9},
    "problem":    {"temperature": 0.8, "max_tokens": 4096, "top_p": 0.95},
    "solution":   {"temperature": 0.2, "max_tokens": 4096, "top_p": 0.9},
    "note":       {"temperature": 0.5, "max_tokens": 2048, "top_p": 0.92},
}
```

## Solar Pro 3 통합 가이드

### API 엔드포인트

- **Chat Completions**: `POST /v1/chat/completions`
  - 지원 파라미터: `model`, `messages`, `temperature`, `max_tokens`, `top_p`, `top_k`, `presence_penalty`, `frequency_penalty`, `stream`
  - System 메시지 지원

- **Document Parse**: `POST /v1/document-ai/document-parse`
  - 지원 파라미터: `document`, `model`, `output_format`, `ocr`, `chart_recognition`, `coordinates`
  - 수학 그래프/차트 인식 지원

- **Information Extract**: `POST /v1/document-ai/extraction`
  - 스키마: 루트가 `object` 타입, `properties` 포함 필요
  - 응답: `result` 키에 추출 데이터

### Agent 구현 패턴

```python
# 1. System Prompt 사용
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": prompt}
]

# 2. 작업별 파라미터 적용
params = GENERATION_PARAMS["task_name"]
response = self.client.chat_completion(
    messages=messages,
    temperature=params["temperature"],
    max_tokens=params["max_tokens"],
    top_p=params["top_p"]
)
```

### 데이터 흐름

dataclass 기반 타입 안전성 확보. 에이전트 간 데이터는 스키마 객체로 전달.

### 에러 처리

각 단계에서 fallback 객체로 graceful degradation 지원. 부분 실패 시에도 계속 진행.
- ExtractorAgent: `result` 키 우선, `extraction` fallback
- 모든 Agent: 예외 발생 시 기본값 반환

### UI 테마

Solar 브랜딩: 주 색상 #FF6B35 (오렌지), 보조 색상 #FFB347 (골드)

## 참고 자료

- [Upstage Console Docs](https://console.upstage.ai/docs)
- [Solar Pro 3 소개](https://upstage.ai/blog/ko/solar-pro-3-0127)
