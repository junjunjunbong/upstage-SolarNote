from agents.base_agent import BaseAgent
from models.schemas import ParsedProblem


class ParserAgent(BaseAgent):
    """Document Parse API를 사용하여 이미지에서 텍스트 추출"""

    def execute(self, file_content: bytes, filename: str) -> ParsedProblem:
        self.log(f"문제 이미지 파싱 중: {filename}")

        result = self.client.document_parse(file_content, filename)

        raw_text = ""
        elements = []
        has_figure = False

        if "content" in result:
            content = result["content"]
            if "text" in content:
                raw_text = content["text"]
            if "elements" in content:
                elements = content["elements"]
                for elem in elements:
                    if elem.get("type") in ["figure", "image", "chart"]:
                        has_figure = True
                        break

        self.log(f"파싱 완료: {len(raw_text)}자 추출")

        return ParsedProblem(
            raw_text=raw_text,
            elements=elements,
            has_figure=has_figure
        )
