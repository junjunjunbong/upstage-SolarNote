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
        print(f"[{self.name}] {message}")
