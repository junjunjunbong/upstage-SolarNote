from agents.base_agent import BaseAgent
from models.schemas import ExtractedFields, ConceptInfo
from prompts.templates import CONCEPT_PROMPT, CONCEPT_SYSTEM_PROMPT
from config import GENERATION_PARAMS


class ConceptAgent(BaseAgent):
    """문제의 개념, 단원, 난이도 분류"""

    def execute(self, extracted: ExtractedFields) -> ConceptInfo:
        self.log("개념 분류 중...")

        prompt = CONCEPT_PROMPT.format(
            problem_text=extracted.problem_text,
            conditions="\n".join(f"- {c}" for c in extracted.conditions) if extracted.conditions else "없음"
        )

        try:
            # Solar Pro 3: system 메시지 + 파라미터 적용
            messages = [
                {"role": "system", "content": CONCEPT_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
            
            params = GENERATION_PARAMS["concept"]
            response = self.client.chat_completion(
                messages=messages,
                temperature=params["temperature"],
                max_tokens=params["max_tokens"],
                top_p=params["top_p"]
            )

            data = self.extract_json(response)

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
