import re
from agents.base_agent import BaseAgent
from models.schemas import ParsedProblem


class ParserAgent(BaseAgent):
    """Document OCR API를 사용하여 이미지에서 텍스트 추출"""

    def _html_to_text(self, html: str) -> str:
        """HTML에서 텍스트만 추출"""
        text = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
        text = re.sub(r'</?(p|h[1-6]|div|li)[^>]*>', '\n', text, flags=re.IGNORECASE)
        text = re.sub(r'<[^>]+>', '', text)
        text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&quot;', '"')
        text = re.sub(r'\n{3,}', '\n\n', text)
        lines = [line.strip() for line in text.split('\n')]
        return '\n'.join(lines).strip()

    def execute(
        self,
        file_content: bytes,
        filename: str,
        use_ocr: bool = True,
        chart_recognition: bool = True
    ) -> ParsedProblem:
        """
        문제 이미지 파싱

        Args:
            file_content: 파일 바이너리
            filename: 파일명
            use_ocr: True면 Document OCR 사용 (수학 문제에 적합), False면 Document Parse 사용
            chart_recognition: Document Parse 사용 시 차트 인식 활성화
        """
        self.log(f"문제 이미지 파싱 중: {filename}")

        raw_text = ""
        elements = []
        has_figure = False

        if use_ocr:
            # Document OCR API 사용 (수학 기호 인식에 더 적합)
            try:
                result = self.client.document_ocr(
                    file_content=file_content,
                    filename=filename
                )

                # pages 배열에서 텍스트 추출
                if "pages" in result:
                    text_parts = []
                    for page in result["pages"]:
                        if page.get("text"):
                            text_parts.append(page["text"])
                    raw_text = "\n".join(text_parts)

                self.log(f"OCR 완료: {len(raw_text)}자 추출")

            except Exception as e:
                self.log(f"OCR 실패, Document Parse로 fallback: {e}")
                use_ocr = False

        if not use_ocr or not raw_text:
            # Document Parse API fallback
            result = self.client.document_parse(
                file_content=file_content,
                filename=filename,
                output_format="markdown",
                ocr="auto",
                chart_recognition=chart_recognition
            )

            if "content" in result:
                content = result["content"]
                if content.get("text"):
                    raw_text = content["text"]
                elif content.get("markdown"):
                    raw_text = content["markdown"]
                elif content.get("html"):
                    raw_text = self._html_to_text(content["html"])

            if "elements" in result:
                elements = result["elements"]
                for elem in elements:
                    if elem.get("category") in ["figure", "image", "chart"]:
                        has_figure = True
                        break

            self.log(f"Parse 완료: {len(raw_text)}자 추출")

        return ParsedProblem(
            raw_text=raw_text,
            elements=elements,
            has_figure=has_figure
        )
