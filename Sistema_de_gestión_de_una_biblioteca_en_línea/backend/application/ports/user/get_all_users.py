from abc import ABC, abstractmethod
from domain.models.user import User
from typing import List


class GetAllUsers(ABC):
    
    @abstractmethod
    async def get_all(self) -> List[User]:
        pass
