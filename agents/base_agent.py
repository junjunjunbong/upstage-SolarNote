import re
import json
from abc import ABC, abstractmethod
from core.upstage_client import UpstageClient


class BaseAgent(ABC):
    """모든 에이전트의 베이스 클래스"""

    def __init__(self, client: UpstageClient):
        self.client = client
        self.name = self.__class__.__name__

    @abstractmethod
    def execute(self, *args, **kwargs):
        """에이전트 실행 메서드 - 서브클래스에서 구현"""
        pass

    def log(self, message: str):
        """간단한 로깅"""
        print(f"[{self.name}] {message}", flush=True)

    def extract_json(self, text: str) -> dict | list:
        """LLM 응답에서 JSON 추출 (```json 블록 또는 순수 JSON)"""
        # 빈 응답 체크
        if not text or not text.strip():
            self.log("경고: 빈 응답 수신")
            raise json.JSONDecodeError("빈 응답", text or "", 0)

        # 1. ```json ... ``` 블록 찾기
        json_block = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
        if json_block:
            json_str = json_block.group(1).strip()
        else:
            # 2. { 또는 [ 로 시작하는 JSON 찾기
            json_match = re.search(r'(\{[\s\S]*\}|\[[\s\S]*\])', text)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = text.strip()

        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # 디버깅을 위한 응답 내용 로깅
            self.log(f"JSON 파싱 실패 - 원본 응답 (앞 500자): {text[:500]}")
            raise e
