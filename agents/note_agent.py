import json
from agents.base_agent import BaseAgent
from models.schemas import ExtractedFields, ConceptInfo, SimilarProblem, SolutionResult, ErrorNote, ProblemSolution
from prompts.templates import NOTE_PROMPT


class NoteAgent(BaseAgent):
    """최종 오답노트 생성"""

    def execute(
        self,
        original: ExtractedFields,
        concept: ConceptInfo,
        problems: list,
        solutions: SolutionResult
    ) -> ErrorNote:
        self.log("오답노트 정리 중...")

        original_solution_text = f"""
풀이 단계: {chr(10).join(f'{i+1}. {s}' for i, s in enumerate(solutions.original.steps))}
정답: {solutions.original.answer}
핵심: {solutions.original.key_point}
"""

        similar_text = ""
        for i, (prob, sol) in enumerate(zip(problems, solutions.similars)):
            similar_text += f"""
[문제 {i+1}] {prob.problem}
유형: {prob.variation_type} | 난이도: {'★' * prob.difficulty}
풀이: {' → '.join(sol.steps) if sol.steps else '없음'}
정답: {sol.answer}
"""

        prompt = NOTE_PROMPT.format(
            original_problem=original.problem_text,
            chapter=concept.chapter,
            topic=concept.topic,
            concepts=", ".join(concept.concepts),
            original_solution=original_solution_text,
            similar_problems_with_solutions=similar_text
        )

        try:
            response = self.client.chat_completion([
                {"role": "user", "content": prompt}
            ])

            data = json.loads(response)

            note = ErrorNote(
                title=data.get("title", concept.topic),
                concept_summary=data.get("concept_summary", ""),
                formula_box=data.get("formula_box", []),
                original_problem=original.problem_text,
                original_solution=solutions.original,
                similar_problems=[
                    {"problem": p, "solution": s}
                    for p, s in zip(problems, solutions.similars)
                ],
                study_tips=data.get("study_tips", ""),
                next_topics=data.get("next_topics", [])
            )

        except Exception as e:
            self.log(f"오답노트 생성 실패: {e}")
            note = ErrorNote(
                title=concept.topic,
                original_problem=original.problem_text,
                original_solution=solutions.original,
                similar_problems=[
                    {"problem": p, "solution": s}
                    for p, s in zip(problems, solutions.similars)
                ]
            )

        self.log("오답노트 완료")
        return note
