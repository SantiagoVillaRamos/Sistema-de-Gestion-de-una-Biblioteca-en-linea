from abc import ABC, abstractmethod
from typing import Optional
from domain.models.user import User

class UserRepository(ABC):
    """
    Define la interfaz para el repositorio de Usuarios.
    """
    @abstractmethod
    async def save(self, user: User) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    async def find_all(self) -> list[User]:
        pass
    
    @abstractmethod
    async def delete(self, user: User) -> None:
        pass
    
    @abstractmethod
    async def find_by_ids(self, user_ids: list[str]) -> list[User]:
        pass