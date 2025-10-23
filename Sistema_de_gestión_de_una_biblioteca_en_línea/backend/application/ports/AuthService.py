from abc import ABC, abstractmethod
from typing import Any

class AuthService(ABC):

    @abstractmethod
    def create_token(self, user_id: str, roles: list[str]) -> str:
        pass

    @abstractmethod
    def validate_token(self, token: str) -> dict[str, Any]:
        pass
