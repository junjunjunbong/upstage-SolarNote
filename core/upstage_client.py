import httpx
from config import UPSTAGE_API_KEY, UPSTAGE_BASE_URL, SOLAR_MODEL, REQUEST_TIMEOUT, DOCUMENT_PARSE_TIMEOUT


class UpstageClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or UPSTAGE_API_KEY
        self.base_url = UPSTAGE_BASE_URL

    def _get_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.api_key}"}

    def chat_completion(
        self,
        messages: list,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None,
        top_p: float = None,
        top_k: int = None,
        presence_penalty: float = None,
        frequency_penalty: float = None,
        stream: bool = False
    ) -> str:
        """
        Solar Chat API - 추론/생성용
        
        Args:
            messages: 대화 메시지 목록 (role, content)
            model: 사용할 모델명 (기본: solar-pro-3)
            temperature: 샘플링 온도 (0~2, 낮을수록 결정적)
            max_tokens: 생성할 최대 토큰 수
            top_p: nucleus 샘플링 (0~1)
            top_k: Top-K 샘플링 (Solar Pro 3 지원)
            presence_penalty: 새로운 토픽 패널티 (-2~2)
            frequency_penalty: 반복 패널티 (-2~2)
            stream: 스트리밍 응답 여부
        
        Returns:
            생성된 텍스트 응답
        """
        model = model or SOLAR_MODEL
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        
        # 선택적 파라미터 추가
        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if top_p is not None:
            payload["top_p"] = top_p
        if top_k is not None:
            payload["top_k"] = top_k
        if presence_penalty is not None:
            payload["presence_penalty"] = presence_penalty
        if frequency_penalty is not None:
            payload["frequency_penalty"] = frequency_penalty
        
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers=self._get_headers(),
            json=payload,
            timeout=REQUEST_TIMEOUT
        )
        if response.status_code != 200:
            raise Exception(f"Chat API 실패 ({response.status_code}): {response.text[:500]}")

        result = response.json()
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")

        # 디버깅: 빈 응답 감지
        if not content or not content.strip():
            print(f"[DEBUG] 빈 응답 감지 - 전체 응답: {result}", flush=True)

        return content

    def document_parse(
        self,
        file_content: bytes,
        filename: str,
        model: str = "document-parse",
        output_format: str = "html",
        ocr: str = "auto",
        chart_recognition: bool = True,
        coordinates: bool = False
    ) -> dict:
        """
        Document Parse API - OCR 및 문서 분석
        
        Args:
            file_content: 파일 바이너리 내용
            filename: 파일명
            model: 모델명 (document-parse, document-parse-nightly)
            output_format: 출력 형식 (html, markdown, text)
            ocr: OCR 모드 (auto, force)
            chart_recognition: 차트/그래프 인식 활성화
            coordinates: 좌표 정보 포함 여부
        
        Returns:
            파싱 결과 딕셔너리
        """
        files = {"document": (filename, file_content)}
        data = {
            "model": model,
            "output_format": output_format,
            "ocr": ocr,
            "chart_recognition": str(chart_recognition).lower(),
        }
        
        if coordinates:
            data["coordinates"] = "true"
        
        response = httpx.post(
            f"{self.base_url}/document-ai/document-parse",
            headers=self._get_headers(),
            files=files,
            data=data,
            timeout=DOCUMENT_PARSE_TIMEOUT
        )
        
        if response.status_code != 200:
            raise Exception(f"Document Parse 실패 (상태코드: {response.status_code}): {response.text[:300]}")
        
        return response.json()

    def document_ocr(
        self,
        file_content: bytes,
        filename: str
    ) -> dict:
        """
        Document OCR API - 순수 텍스트 추출 (수학 기호에 더 적합)

        Args:
            file_content: 파일 바이너리 내용
            filename: 파일명

        Returns:
            OCR 결과 딕셔너리 (pages 배열 포함)
        """
        files = {"document": (filename, file_content)}
        data = {"model": "ocr"}

        response = httpx.post(
            f"{self.base_url}/document-digitization",
            headers=self._get_headers(),
            files=files,
            data=data,
            timeout=DOCUMENT_PARSE_TIMEOUT
        )

        if response.status_code != 200:
            raise Exception(f"Document OCR 실패 ({response.status_code}): {response.text[:300]}")

        return response.json()

    def information_extract(
        self,
        text: str,
        schema: dict,
        model: str = None
    ) -> dict:
        """
        Information Extract API - 필드 추출용
        
        Args:
            text: 추출할 원본 텍스트
            schema: JSON Schema 형식의 출력 구조 정의
            model: 사용 모델 (선택적)
        
        Returns:
            추출 결과 딕셔너리 (result 키 포함)
        """
        payload = {
            "text": text,
            "schema": schema
        }
        
        if model:
            payload["model"] = model
        
        response = httpx.post(
            f"{self.base_url}/document-ai/extraction",
            headers=self._get_headers(),
            json=payload,
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
