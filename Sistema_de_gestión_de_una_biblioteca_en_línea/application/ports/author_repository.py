from abc import ABC, abstractmethod
from typing import Optional, List
from domain.models.author import Author


class AuthorRepository(ABC):
    """
    Interfaz para el repositorio de Autores.
    """
    @abstractmethod
    async def save(self, author: Author) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, author_id: str) -> Optional[Author]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Author]:
        pass

    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[Author]:
        pass

    @abstractmethod
    async def find_by_ids(self, author_ids: List[str]) -> List[Author]:
        """Busca una lista de autores por sus IDs."""
        pass
    
    @abstractmethod
    async def update(self, author: Author) -> None:
        """Actualiza la información de un autor existente."""
        pass