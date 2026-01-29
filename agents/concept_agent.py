import json
from agents.base_agent import BaseAgent
from models.schemas import ExtractedFields, ConceptInfo
from prompts.templates import CONCEPT_PROMPT


class ConceptAgent(BaseAgent):
    """문제의 개념, 단원, 난이도 분류"""

    def execute(self, extracted: ExtractedFields) -> ConceptInfo:
        self.log("개념 분류 중...")

        prompt = CONCEPT_PROMPT.format(
            problem_text=extracted.problem_text,
            conditions="\n".join(f"- {c}" for c in extracted.conditions) if extracted.conditions else "없음"
        )

        try:
            response = self.client.chat_completion([
                {"role": "user", "content": prompt}
            ])

            data = json.loads(response)

            concept = ConceptInfo(
                subject=data.get("subject", "수학"),
                chapter=data.get("chapter", ""),
                topic=data.get("topic", ""),
                concepts=data.get("concepts", []),
                difficulty=data.get("difficulty", 3),
                prerequisites=data.get("prerequisites", [])
            )

        except Exception as e:
            self.log(f"분류 실패, 기본값 사용: {e}")
            concept = ConceptInfo(topic="일반", difficulty=3)

        self.log(f"분류 완료: {concept.topic} (난이도 {concept.difficulty})")
        return concept
