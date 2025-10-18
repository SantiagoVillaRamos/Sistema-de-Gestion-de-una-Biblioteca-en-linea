from typing import Dict, Optional, List
from application.ports.book_repository import BookRepository
from domain.models.book import Book
from domain.models.value_objects.isbn import ISBN
from infrastructure.mapper_infrastructure.book_mapper import BookMapper

from domain.models.exceptions.business_exception import BusinessConflictError, BusinessNotFoundError

class BookInMemoryRepository(BookRepository):
    
    def __init__(self):
        # Almacenamos diccionarios, no objetos Book directamente.
        self._books: Dict[str, dict] = {}

    async def save(self, book: Book) -> None:
        book_exists = any(b['isbn'] == book.isbn.value for b in self._books.values())
        if book_exists:
            raise BusinessConflictError(book.isbn.value, "El libro con este ISBN ya existe")
        persistence_data = BookMapper.to_persistence(book)
        self._books[book.book_id] = persistence_data
        
        
    async def update(self, book: Book) -> None:
        if book.book_id not in self._books:
            raise BusinessNotFoundError(book.book_id, "El ID no existe")
        persistence_data = BookMapper.to_persistence(book)
        self._books[book.book_id] = persistence_data


    async def find_by_id(self, book_id: str) -> Optional[Book]:
        persistence_data = self._books.get(book_id)
        if not persistence_data:
            raise BusinessNotFoundError(book_id, "El ID no existe")
        return BookMapper.to_domain(persistence_data)


    async def find_by_isbn(self, isbn: ISBN) -> Optional[Book]:
        persistence_data = next((b for b in self._books.values() if b['isbn'] == isbn.value), None)
        if not persistence_data:
            raise BusinessNotFoundError(isbn.value, "El ISBN no existe")
        return BookMapper.to_domain(persistence_data)
    
    
    async def find_by_ids(self, book_ids: List[str]) -> List[Book]:
        books_data = [self._books[book_id] for book_id in book_ids if book_id in self._books]
        return [BookMapper.to_domain(data) for data in books_data]


    async def get_all(self) -> List[Book]:
        if not self._books:
            return []
        return [BookMapper.to_domain(data) for data in self._books.values()]

    async def delete(self, book: Book) -> None:
        if book.book_id not in self._books:
            raise BusinessNotFoundError(book.book_id, "El ID no existe")
        else:
            del self._books[book.book_id]
            
            