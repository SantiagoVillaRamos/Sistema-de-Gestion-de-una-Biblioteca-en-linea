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
