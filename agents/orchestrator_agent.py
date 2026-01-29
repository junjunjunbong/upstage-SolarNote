from typing import Callable
from config import MAX_RETRIES
from core.upstage_client import UpstageClient
from models.schemas import ErrorNote
from agents.parser_agent import ParserAgent
from agents.extractor_agent import ExtractorAgent
from agents.concept_agent import ConceptAgent
from agents.problem_agent import ProblemAgent
from agents.solution_agent import SolutionAgent
from agents.note_agent import NoteAgent


class OrchestratorAgent:
    """전체 워크플로우를 조율하는 총괄 에이전트"""

    def __init__(self, client: UpstageClient = None):
        self.client = client or UpstageClient()
        self.parser = ParserAgent(self.client)
        self.extractor = ExtractorAgent(self.client)
        self.concept = ConceptAgent(self.client)
        self.problem = ProblemAgent(self.client)
        self.solution = SolutionAgent(self.client)
        self.note = NoteAgent(self.client)
        self.progress_callback = None

    def set_progress_callback(self, callback: Callable[[int, int, str], None]):
        """진행 상태 콜백 설정"""
        self.progress_callback = callback

    def _update_progress(self, step: int, total: int, message: str):
        """진행 상태 업데이트"""
        if self.progress_callback:
            self.progress_callback(step, total, message)
        print(f"[{step}/{total}] {message}")

    def _with_retry(self, func: Callable, max_retries: int = None):
        """재시도 로직"""
        max_retries = max_retries or MAX_RETRIES
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                return func()
            except Exception as e:
                last_error = e
                if attempt < max_retries:
                    print(f"재시도 {attempt + 1}/{max_retries}: {e}")

        raise last_error

    def execute(self, file_content: bytes, filename: str, options: dict = None) -> dict:
        """전체 워크플로우 실행"""
        options = options or {}
        total_steps = 6

        try:
            # 1. 문제 파싱 (필수 - 실패 시 중단)
            self._update_progress(1, total_steps, "이미지에서 문제 추출 중...")
            parsed = self.parser.execute(file_content, filename)

            if not parsed or not parsed.raw_text:
                return {
                    "success": False,
                    "error": "이미지에서 문제를 인식할 수 없습니다"
                }

            # 2. 필드 추출 (실패 시 raw_text로 fallback)
            self._update_progress(2, total_steps, "문제 구성요소 분석 중...")
            try:
                extracted = self.extractor.execute(parsed)
            except Exception:
                from models.schemas import ExtractedFields
                extracted = ExtractedFields(problem_text=parsed.raw_text)

            # 3. 개념 분류 (실패 시 기본값)
            self._update_progress(3, total_steps, "개념 및 단원 분류 중...")
            try:
                concept = self.concept.execute(extracted)
            except Exception:
                from models.schemas import ConceptInfo
                concept = ConceptInfo(topic="일반", difficulty=3)

            # 4. 유사문제 생성 (재시도 로직)
            self._update_progress(4, total_steps, "유사문제 생성 중...")
            problems = self._with_retry(
                lambda: self.problem.execute(extracted, concept, options)
            )

            # 5. 풀이 작성 (재시도 로직)
            self._update_progress(5, total_steps, "상세 풀이 작성 중...")
            solutions = self._with_retry(
                lambda: self.solution.execute(extracted, problems, concept)
            )

            # 6. 오답노트 정리
            self._update_progress(6, total_steps, "오답노트 정리 중...")
            note = self._with_retry(
                lambda: self.note.execute(
                    original=extracted,
                    concept=concept,
                    problems=problems,
                    solutions=solutions
                )
            )

            return {
                "success": True,
                "note": note,
                "concept": concept,
                "problems_count": len(problems)
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"처리 중 오류가 발생했습니다: {str(e)}"
            }
