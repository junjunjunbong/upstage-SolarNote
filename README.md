# 📝 수학 오답노트 자동 생성기

학생이 틀린 수학 문제 사진을 업로드하면 **유사문제 5개**와 **상세 풀이**를 자동으로 생성하는 AI 멀티 에이전트 시스템입니다.

## 주요 기능

- 📷 **문제 이미지 인식**: 수학 문제 사진에서 텍스트/수식 자동 추출
- 🧠 **개념 분류**: 단원, 핵심 개념, 난이도 자동 분류
- 🔄 **유사문제 생성**: 숫자변형, 개념확장, 역문제, 응용, 심화 5가지 유형
- ✏️ **상세 풀이**: 원본 + 유사문제 단계별 풀이 제공
- 📋 **오답노트 정리**: 학습 조언, 공식 정리, 다음 학습 추천

## 기술 스택

- **Frontend**: Streamlit
- **Backend**: Python
- **AI API**: Upstage (Solar, Document Parse, Information Extract)

## 설치 및 실행

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. API 키 설정
# .env 파일에 Upstage API 키 입력
UPSTAGE_API_KEY=your_api_key_here

# 3. 앱 실행
streamlit run app.py
```

## 프로젝트 구조

```
upstage-project/
├── app.py                    # Streamlit 메인 앱
├── config.py                 # 환경 설정
├── agents/                   # 멀티 에이전트
│   ├── base_agent.py         # 베이스 에이전트 클래스
│   ├── orchestrator_agent.py # 총괄 에이전트
│   ├── parser_agent.py       # 이미지 → 텍스트 (Document Parse)
│   ├── extractor_agent.py    # 필드 추출 (Information Extract)
│   ├── concept_agent.py      # 개념 분류 (Solar)
│   ├── problem_agent.py      # 유사문제 생성 (Solar)
│   ├── solution_agent.py     # 풀이 작성 (Solar)
│   └── note_agent.py         # 오답노트 정리 (Solar)
├── core/
│   └── upstage_client.py     # Upstage API 클라이언트
├── models/
│   └── schemas.py            # 데이터 모델
├── prompts/
│   └── templates.py          # 프롬프트 템플릿
└── ui/
    └── components.py         # UI 컴포넌트
```

## 에이전트 파이프라인

```
이미지 → Parser → Extractor → Concept → Problem → Solution → Note → 오답노트
         (OCR)   (필드분리)   (분류)   (생성)    (풀이)    (정리)
```

## API 사용량

| API | 역할 | 호출 횟수 |
|-----|------|----------|
| Document Parse | OCR | 1회 |
| Information Extract | 필드 추출 | 1회 |
| Solar | LLM (분류/생성/풀이/정리) | 4회 |

**총**: 문제 1개당 약 6회 API 호출

## 타겟 사용자

- 과외 선생님
- 자기주도 학습 학생

## 라이선스

MIT License
