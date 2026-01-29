import httpx
from config import UPSTAGE_API_KEY, UPSTAGE_BASE_URL, SOLAR_MODEL, REQUEST_TIMEOUT, DOCUMENT_PARSE_TIMEOUT


class UpstageClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or UPSTAGE_API_KEY
        self.base_url = UPSTAGE_BASE_URL

    def _get_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.api_key}"}

    def chat_completion(self, messages: list, model: str = None) -> str:
        """Solar Chat API - 추론/생성용"""
        model = model or SOLAR_MODEL
        response = httpx.post(
            f"{self.base_url}/solar/chat/completions",
            headers=self._get_headers(),
            json={"model": model, "messages": messages},
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def document_parse(self, file_content: bytes, filename: str) -> dict:
        """Document Parse API - OCR용"""
        response = httpx.post(
            f"{self.base_url}/document-ai/document-parse",
            headers=self._get_headers(),
            files={"document": (filename, file_content)},
            timeout=DOCUMENT_PARSE_TIMEOUT
        )
        response.raise_for_status()
        return response.json()

    def information_extract(self, text: str, schema: dict) -> dict:
        """Information Extract API - 필드 추출용"""
        response = httpx.post(
            f"{self.base_url}/document-ai/extraction",
            headers=self._get_headers(),
            json={"text": text, "schema": schema},
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
