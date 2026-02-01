# ========== System Prompts ==========
# 각 에이전트별 역할 정의 (Solar Pro 3의 system 메시지 활용)

CONCEPT_SYSTEM_PROMPT = """당신은 수학 교육 전문가입니다. 학생들이 효과적으로 학습할 수 있도록 수학 문제를 정확하게 분석하고 분류하는 역할을 합니다."""

PROBLEM_SYSTEM_PROMPT = """당신은 수학 문제 출제 전문가입니다. 학생의 학습 수준에 맞는 적절한 난이도의 유사문제를 생성하는 역할을 합니다. 원본 문제의 핵심 개념을 유지하면서 다양한 변형을 만드는 것이 전문 분야입니다."""

SOLUTION_SYSTEM_PROMPT = """당신은 수학 강사입니다. 학생들이 쉽게 이해할 수 있도록 단계별로 명확하게 설명하는 것이 전문 분야입니다. 모든 풀이는 논리적이고 검증 가능해야 합니다."""

NOTE_SYSTEM_PROMPT = """당신은 수학 학습 코치입니다. 학생들의 오답을 분석하고 효과적인 학습 전략을 제시하는 역할을 합니다. 핵심 개념을 요약하고 다음 학습 방향을 안내합니다."""


# ========== User Prompts ==========

CONCEPT_PROMPT = """다음 수학 문제를 분석하여 JSON 형식으로 정보를 추출하세요.

## 문제
{problem_text}

## 조건
{conditions}

## 출력 형식 (JSON)
{{
    "subject": "수학1/수학2/미적분/확률과통계/기하 중 하나",
    "chapter": "단원명 (예: 지수함수와 로그함수)",
    "topic": "세부 주제 (예: 지수법칙의 활용)",
    "concepts": ["핵심 개념1", "핵심 개념2"],
    "difficulty": 1-5 사이 정수 (1: 매우 쉬움, 5: 매우 어려움),
    "prerequisites": ["선수 개념1", "선수 개념2"]
}}

JSON만 출력하세요."""


PROBLEM_PROMPT = """주어진 원본 문제와 동일한 개념을 다루는 유사문제 {problem_count}개를 생성하세요.

## 원본 문제
{problem_text}

## 개념 정보
- 단원: {chapter}
- 주제: {topic}
- 핵심 개념: {concepts}
- 난이도: {difficulty}/5

## 생성 조건
{generation_conditions}

## 출력 형식 (JSON 배열)
[
    {{
        "problem": "문제 텍스트",
        "difficulty": 1-5,
        "variation_type": "숫자변형|개념확장|역문제|응용|심화",
        "hint": "힌트 (핵심 접근법만 간단히)"
    }}
]

JSON 배열만 출력하세요."""


SOLUTION_PROMPT = """주어진 문제들의 상세한 풀이를 작성하세요.

## 원본 문제
{original_problem}

## 유사문제들
{similar_problems}

## 개념 정보
- 주제: {topic}
- 핵심 개념: {concepts}

## 풀이 작성 지침
1. 원본 문제: 가장 상세하게 단계별 풀이
2. 유사문제: 각각 간결하지만 명확한 풀이
3. 모든 풀이는 수학적으로 정확해야 함
4. 중간 계산 과정 반드시 포함

## 출력 형식 (JSON)
{{
    "original": {{
        "steps": ["풀이 단계1", "풀이 단계2", ...],
        "answer": "최종 답",
        "key_point": "핵심 포인트 (1-2문장)"
    }},
    "similars": [
        {{
            "steps": ["풀이 단계1", ...],
            "answer": "최종 답",
            "key_point": "핵심 포인트"
        }}
    ]
}}

JSON만 출력하세요."""


NOTE_PROMPT = """학생을 위한 오답노트를 작성하세요.

## 원본 문제
{original_problem}

## 개념 정보
- 단원: {chapter}
- 주제: {topic}
- 핵심 개념: {concepts}

## 원본 풀이
{original_solution}

## 유사문제 및 풀이
{similar_problems_with_solutions}

## 출력 형식 (JSON)
{{
    "title": "오답노트 제목 (예: 이차방정식의 근과 계수의 관계)",
    "concept_summary": "개념 요약 설명 (2-3문장, 핵심만)",
    "formula_box": ["공식1", "공식2", "공식3"],
    "study_tips": "학습 조언 (2-3문장, 실수 방지법 중심)",
    "next_topics": ["다음 학습 추천 주제1", "주제2"]
}}

JSON만 출력하세요."""


# ========== Information Extraction Schema ==========
# 공식 문서: 루트는 반드시 object 타입, properties 포함
# https://console.upstage.ai/docs

EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "problem_text": {
            "type": "string",
            "description": "문제 본문 (조건과 질문을 포함한 전체 텍스트)"
        },
        "conditions": {
            "type": "array",
            "description": "문제에서 주어진 조건들의 목록",
            "items": {
                "type": "string",
                "description": "개별 조건"
            }
        },
        "choices": {
            "type": "array",
            "description": "객관식 보기 (있는 경우). 없으면 빈 배열",
            "items": {
                "type": "string",
                "description": "보기 텍스트"
            }
        },
        "points": {
            "type": "integer",
            "description": "배점 (명시되지 않은 경우 null)"
        },
        "answer_type": {
            "type": "string",
            "description": "답안 유형: 객관식/서술형/단답형/선다형 중 하나"
        },
        "figure_description": {
            "type": "string",
            "description": "첨부 그림/도형에 대한 설명 (있는 경우). 없으면 null"
        }
    },
    "required": ["problem_text", "answer_type"]
}
