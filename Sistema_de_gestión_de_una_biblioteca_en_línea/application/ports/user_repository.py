from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.user import User

class UserRepository(ABC):
    """
    Define la interfaz para el repositorio de Usuarios.
    """
    @abstractmethod
    async def save(self, user: User) -> None:
        """Guarda un usuario nuevo o actualiza uno existente."""
        pass

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Busca un usuario por su ID."""
        pass