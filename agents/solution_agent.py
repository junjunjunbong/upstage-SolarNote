from agents.base_agent import BaseAgent
from models.schemas import ExtractedFields, ConceptInfo, SimilarProblem, ProblemSolution, SolutionResult
from prompts.templates import SOLUTION_PROMPT, SOLUTION_SYSTEM_PROMPT
from config import GENERATION_PARAMS


class SolutionAgent(BaseAgent):
    """원본 + 유사문제 풀이 작성"""

    def execute(self, extracted: ExtractedFields, problems: list, concept: ConceptInfo) -> SolutionResult:
        self.log("풀이 작성 중...")

        similar_text = "\n".join([
            f"{i+1}. [{p.variation_type}] {p.problem}"
            for i, p in enumerate(problems)
        ])

        prompt = SOLUTION_PROMPT.format(
            original_problem=extracted.problem_text,
            similar_problems=similar_text,
            topic=concept.topic,
            concepts=", ".join(concept.concepts)
        )

        try:
            # Solar Pro 3: system 메시지 + 파라미터 적용
            messages = [
                {"role": "system", "content": SOLUTION_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
            
            params = GENERATION_PARAMS["solution"]
            response = self.client.chat_completion(
                messages=messages,
                temperature=params["temperature"],
                max_tokens=params["max_tokens"],
                top_p=params["top_p"]
            )

            data = self.extract_json(response)

            original_data = data.get("original", {})
            original_solution = ProblemSolution(
                steps=original_data.get("steps", []),
                answer=original_data.get("answer", ""),
                key_point=original_data.get("key_point", "")
            )

            similar_solutions = [
                ProblemSolution(
                    steps=s.get("steps", []),
                    answer=s.get("answer", ""),
                    key_point=s.get("key_point", "")
                )
                for s in data.get("similars", [])
            ]

            result = SolutionResult(
                original=original_solution,
                similars=similar_solutions
            )

        except Exception as e:
            self.log(f"풀이 작성 실패: {e}")
            result = SolutionResult()

        self.log("풀이 작성 완료")
        return result
