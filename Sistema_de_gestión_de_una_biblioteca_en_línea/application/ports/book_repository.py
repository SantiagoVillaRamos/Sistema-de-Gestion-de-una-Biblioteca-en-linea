from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.book import Book
from domain.value_objects.isbn import ISBN


class BookRepository(ABC):
    """
    Define la interfaz para el repositorio de Libros.
    """
    @abstractmethod
    async def save(self, book: Book) -> None:
        """Guarda un libro nuevo o actualiza uno existente."""
        pass
    
    @abstractmethod
    async def update(self, book: Book) -> None:
        """Actualiza un libro existente."""
        pass

    @abstractmethod
    async def find_by_id(self, book_id: str) -> Optional[Book]:
        """Busca un libro por su ID."""
        pass
    
    @abstractmethod
    async def find_by_ids(self, book_ids: List[str]) -> List[Book]:
        """Busca y devuelve una lista de libros por sus IDs."""
        pass

    @abstractmethod
    async def get_all(self) -> List[Book]:
        """Obtiene todos los libros."""
        pass