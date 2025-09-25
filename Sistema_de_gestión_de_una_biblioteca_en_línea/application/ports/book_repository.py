from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.book import Book
from domain.value_objects.isbn import ISBN


class BookRepository(ABC):
    """
    Interfaz para el repositorio de Libros.
    """
    @abstractmethod
    async def save(self, book: Book) -> None:
        pass
    
    @abstractmethod
    async def update(self, book: Book) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, book_id: str) -> Optional[Book]:
        pass
    
    @abstractmethod
    async def find_by_ids(self, book_ids: List[str]) -> List[Book]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Book]:
        pass