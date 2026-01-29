CONCEPT_PROMPT = """당신은 수학 교육 전문가입니다. 주어진 수학 문제를 분석하여 다음 정보를 JSON 형식으로 추출하세요.

## 문제
{problem_text}

## 조건
{conditions}

## 출력 형식 (JSON)
{{
    "subject": "수학1/수학2/미적분/확률과통계/기하 중 하나",
    "chapter": "단원명",
    "topic": "세부 주제",
    "concepts": ["핵심 개념1", "핵심 개념2"],
    "difficulty": 1-5 사이 정수,
    "prerequisites": ["선수 개념1", "선수 개념2"]
}}

JSON만 출력하세요."""


PROBLEM_PROMPT = """당신은 수학 문제 출제 전문가입니다. 주어진 원본 문제와 동일한 개념을 다루는 유사문제 5개를 생성하세요.

## 원본 문제
{problem_text}

## 개념 정보
- 단원: {chapter}
- 주제: {topic}
- 핵심 개념: {concepts}
- 난이도: {difficulty}/5

## 생성 조건
- 숫자변형: 숫자만 바꾼 문제 1개
- 개념확장: 같은 개념의 다른 형태 1개
- 역문제: 조건과 답을 바꾼 문제 1개
- 응용: 실생활 적용 문제 1개
- 심화: 난이도 높인 문제 1개

## 출력 형식 (JSON 배열)
[
    {{
        "problem": "문제 텍스트",
        "difficulty": 1-5,
        "variation_type": "숫자변형|개념확장|역문제|응용|심화",
        "hint": "힌트"
    }}
]

JSON 배열만 출력하세요."""


SOLUTION_PROMPT = """당신은 수학 강사입니다. 주어진 문제들의 상세한 풀이를 작성하세요.

## 원본 문제
{original_problem}

## 유사문제들
{similar_problems}

## 개념 정보
- 주제: {topic}
- 핵심 개념: {concepts}

## 출력 형식 (JSON)
{{
    "original": {{
        "steps": ["풀이 단계1", "풀이 단계2", ...],
        "answer": "최종 답",
        "key_point": "핵심 포인트"
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


NOTE_PROMPT = """당신은 수학 교육 전문가입니다. 학생을 위한 오답노트를 작성하세요.

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
    "concept_summary": "개념 요약 설명 (2-3문장)",
    "formula_box": ["공식1", "공식2"],
    "study_tips": "학습 조언 (2-3문장)",
    "next_topics": ["다음 학습 추천 주제1", "주제2"]
}}

JSON만 출력하세요."""


EXTRACTION_SCHEMA = {
    "problem_text": {"type": "string", "description": "문제 본문"},
    "conditions": {"type": "array", "description": "문제 조건들"},
    "choices": {"type": "array", "description": "객관식 보기 (있는 경우)"},
    "points": {"type": "integer", "description": "배점"},
    "answer_type": {"type": "string", "description": "답안 유형: 객관식/서술형/단답형"},
    "figure_description": {"type": "string", "description": "그림 설명 (있는 경우)"}
}
