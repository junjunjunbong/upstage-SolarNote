import json
from agents.base_agent import BaseAgent
from models.schemas import ParsedProblem, ExtractedFields
from prompts.templates import EXTRACTION_SCHEMA


class ExtractorAgent(BaseAgent):
    """파싱된 텍스트에서 문제 구성요소 추출"""

    def execute(self, parsed: ParsedProblem) -> ExtractedFields:
        self.log("필드 추출 중...")

        try:
            result = self.client.information_extract(
                text=parsed.raw_text,
                schema=EXTRACTION_SCHEMA
            )

            # 공식 API 응답: result 키에 실제 데이터가 있음
            # https://console.upstage.ai/docs
            data = result.get("result", {})
            
            # result가 비어있으면 extraction 키 fallback (이전 버전 호환)
            if not data:
                data = result.get("extraction", {})

            extracted = ExtractedFields(
                problem_text=data.get("problem_text", parsed.raw_text),
                conditions=data.get("conditions", []),
                choices=data.get("choices", []),
                points=data.get("points"),
                answer_type=data.get("answer_type", "서술형"),
                figure_description=data.get("figure_description")
            )

        except Exception as e:
            self.log(f"추출 실패, fallback 사용: {e}")
            extracted = ExtractedFields(problem_text=parsed.raw_text)

        self.log(f"추출 완료: {extracted.answer_type}")
        return extracted
