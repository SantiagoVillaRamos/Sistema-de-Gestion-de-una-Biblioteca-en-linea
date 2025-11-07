from abc import ABC, abstractmethod
from application.dto.user_command_dto import UserDetailsDTO
from typing import Optional


class GetUser(ABC):
    
    @abstractmethod
    async def get_user(self, user_id: str) -> Optional[UserDetailsDTO]:
        pass