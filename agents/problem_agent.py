import json
from agents.base_agent import BaseAgent
from models.schemas import ExtractedFields, ConceptInfo, SimilarProblem
from prompts.templates import PROBLEM_PROMPT


class ProblemAgent(BaseAgent):
    """유사문제 5개 생성"""

    def execute(self, extracted: ExtractedFields, concept: ConceptInfo, options: dict = None) -> list:
        self.log("유사문제 생성 중...")

        options = options or {}
        difficulty = options.get("difficulty", concept.difficulty)

        prompt = PROBLEM_PROMPT.format(
            problem_text=extracted.problem_text,
            chapter=concept.chapter,
            topic=concept.topic,
            concepts=", ".join(concept.concepts),
            difficulty=difficulty
        )

        try:
            response = self.client.chat_completion([
                {"role": "user", "content": prompt}
            ])

            data = json.loads(response)

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
