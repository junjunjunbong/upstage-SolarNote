# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

SolarNote는 수학 문제 이미지를 분석하여 오답 노트를 자동 생성하는 AI 애플리케이션입니다. Streamlit 프론트엔드와 Upstage API(Solar LLM, Document Parse, Information Extract)를 사용합니다.

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
    ├── ParserAgent      → Document Parse API (OCR)
    ├── ExtractorAgent   → Information Extract API (필드 추출)
    ├── ConceptAgent     → Solar LLM (주제/난이도 분류)
    ├── ProblemAgent     → Solar LLM (유사 문제 5개 생성)
    ├── SolutionAgent    → Solar LLM (풀이 작성)
    └── NoteAgent        → Solar LLM (오답 노트 생성)
    → 최종 오답 노트 출력
```

### 폴더 구조

- `agents/` - 6개의 특화된 에이전트 클래스 (BaseAgent 상속)
- `core/upstage_client.py` - Upstage API 래퍼 (chat_completion, document_parse, information_extract)
- `models/schemas.py` - 7개의 dataclass 스키마 (ParsedProblem, ExtractedFields, ConceptInfo 등)
- `prompts/templates.py` - LLM 프롬프트 템플릿 (CONCEPT_PROMPT, PROBLEM_PROMPT 등)
- `ui/` - Streamlit UI 컴포넌트 및 CSS 스타일링

### 주요 설정값 (config.py)

- `SOLAR_MODEL = "solar-pro"` - 사용 LLM 모델
- `REQUEST_TIMEOUT = 60.0` / `DOCUMENT_PARSE_TIMEOUT = 120.0` - API 타임아웃
- `MAX_RETRIES = 2` - 재시도 횟수

## 코드 패턴

### Agent 구현
모든 에이전트는 `BaseAgent`를 상속하고 단일 책임 원칙을 따름. `OrchestratorAgent._with_retry()` 메서드로 중요 작업 재시도 처리.

### 데이터 흐름
dataclass 기반 타입 안전성 확보. 에이전트 간 데이터는 스키마 객체로 전달.

### 에러 처리
각 단계에서 fallback 객체로 graceful degradation 지원. 부분 실패 시에도 계속 진행.

### UI 테마
Solar 브랜딩: 주 색상 #FF6B35 (오렌지), 보조 색상 #FFB347 (골드)
