from typing import Dict, Optional, List
from application.ports.book_repository import BookRepository
from domain.entities.book import Book
from domain.value_objects.isbn import ISBN

from domain.exceptions.book import BookAlreadyExistsError, BookNotFoundError

class BookInMemoryRepository(BookRepository):
    """
    Implementación del repositorio de libros que almacena los datos en memoria.
    """
    def __init__(self):
        # Usamos un diccionario para un acceso rápido por ID
        self._books: Dict[str, Book] = {}

    async def save(self, book: Book) -> None:
        book_exists = any(b for b in self._books.values() if b.isbn == book.isbn)
        if book_exists:
            raise BookAlreadyExistsError(book.isbn.value)
        self._books[book.book_id] = book
        
    async def update(self, book: Book) -> None:
        if book.book_id not in self._books:
            raise BookNotFoundError(book.book_id, "El ID no existe")
        self._books[book.book_id] = book

    async def find_by_id(self, book_id: str) -> Optional[Book]:
        book = self._books.get(book_id)
        if not book:
            raise BookNotFoundError(book_id, "El ID no existe")
        return book

    async def find_by_isbn(self, isbn: ISBN) -> Optional[Book]:
        book = next((b for b in self._books.values() if b.isbn == isbn), None)
        if not book:
            raise BookNotFoundError(isbn.value, "El ISBN no existe")
        return book
    
    async def find_by_ids(self, book_ids: List[str]) -> List[Book]:
        
        books = [self._books[book_id] for book_id in book_ids if book_id in self._books]
        return books

    async def get_all(self) -> List[Book]:
        if not self._books:
            return []
        return list(self._books.values())
        
    
    
    