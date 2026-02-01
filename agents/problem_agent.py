from agents.base_agent import BaseAgent
from models.schemas import ExtractedFields, ConceptInfo, SimilarProblem
from prompts.templates import PROBLEM_PROMPT, PROBLEM_SYSTEM_PROMPT
from config import GENERATION_PARAMS


class ProblemAgent(BaseAgent):
    """유사문제 생성 (개수 옵션 지원)"""

    def _build_generation_conditions(self, count: int) -> str:
        """문제 개수에 따른 생성 조건 텍스트 생성"""
        conditions = [
            ("숫자변형", "숫자만 바꾼 문제", "난이도 유지"),
            ("개념확장", "같은 개념의 다른 형태", "난이도 유지"),
            ("역문제", "조건과 답을 바꾼 문제", "난이도 약간 상승"),
            ("응용", "실생활 적용 문제", "난이도 유지"),
            ("심화", "난이도 높인 문제", "난이도 상승"),
        ]

        # count에 맞게 조건 선택 (최대 5개)
        selected = conditions[:min(count, len(conditions))]

        # 남은 개수가 있으면 숫자변형/개념확장 순으로 추가
        while len(selected) < count:
            idx = (len(selected) - len(conditions)) % 2
            base = conditions[idx]
            selected.append((base[0], base[1], base[2]))

        lines = []
        for i, (var_type, desc, diff) in enumerate(selected, 1):
            lines.append(f"{i}. {var_type}: {desc} 1개 ({diff})")

        return "\n".join(lines)

    def execute(self, extracted: ExtractedFields, concept: ConceptInfo, options: dict = None) -> list:
        options = options or {}
        problem_count = options.get("problem_count", 5)
        difficulty = options.get("difficulty", concept.difficulty)

        self.log(f"유사문제 {problem_count}개 생성 중...")

        generation_conditions = self._build_generation_conditions(problem_count)

        prompt = PROBLEM_PROMPT.format(
            problem_text=extracted.problem_text,
            chapter=concept.chapter,
            topic=concept.topic,
            concepts=", ".join(concept.concepts),
            difficulty=difficulty,
            problem_count=problem_count,
            generation_conditions=generation_conditions
        )

        try:
            # Solar Pro 3: system 메시지 + 파라미터 적용
            messages = [
                {"role": "system", "content": PROBLEM_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
            
            params = GENERATION_PARAMS["problem"]
            response = self.client.chat_completion(
                messages=messages,
                temperature=params["temperature"],
                max_tokens=params["max_tokens"],
                top_p=params["top_p"]
            )

            data = self.extract_json(response)

            problems = [
                SimilarProblem(
                    problem=p.get("problem", ""),
                    difficulty=p.get("difficulty", 3),
                    variation_type=p.get("variation_type", "숫자변형"),
                    hint=p.get("hint", "")
                )
                for p in data
            ]

        except Exception as e:
            self.log(f"생성 실패: {e}")
            problems = []

        self.log(f"생성 완료: {len(problems)}개 문제")
        return problems
