from typing import Dict, Optional, List
from domain.ports.book_repository import BookRepository
from domain.models.book import Book
from domain.models.value_objects.isbn import ISBN
from domain.models.value_objects.title import Title
from infrastructure.mapper_infrastructure.book_mapper import BookMapper


class BookInMemoryRepository(BookRepository):
    
    def __init__(self):
        # Almacenamos diccionarios, no objetos Book directamente.
        self._books: Dict[str, dict] = {}

    async def save(self, book: Book) -> None:
        persistence_data = BookMapper.to_persistence(book)
        self._books[book.book_id] = persistence_data
        
        
    async def update(self, book: Book) -> None:
        persistence_data = BookMapper.to_persistence(book)
        self._books[book.book_id] = persistence_data


    async def find_by_id(self, book_id: str) -> Optional[Book]:
        persistence_data = self._books.get(book_id)
        return BookMapper.to_domain(persistence_data)


    async def find_by_isbn(self, isbn: ISBN) -> Optional[Book]:
        persistence_data = next((b for b in self._books.values() if b['isbn'] == isbn.value), None)
        return BookMapper.to_domain(persistence_data)
    
    
    async def find_by_title(self, title: Title) -> Optional[Book]:
        persistence_data = next((b for b in self._books.values() if b['title'] == title.value), None)
        return BookMapper.to_domain(persistence_data)
        
    
    async def find_by_ids(self, book_ids: List[str]) -> List[Book]:
        books_data = [self._books[book_id] for book_id in book_ids if book_id in self._books]
        return [BookMapper.to_domain(data) for data in books_data]


    async def get_all(self) -> List[Book]:
        if not self._books:
            return []
        return [BookMapper.to_domain(data) for data in self._books.values()]


    async def delete(self, book: Book) -> None:
        del self._books[book.book_id]
            
            
    async def find_by_author_id(self, author_id: str) -> List[Book]:
    
        # Busca en todos los libros aquellos donde author_id esté en la lista de autores
        books_data = [
            data for data in self._books.values() 
            if author_id in data['author'] 
        ]
        
        return [BookMapper.to_domain(data) for data in books_data]
            
            
    async def count_by_author_id(self, author_id: str) -> int:
        """Cuenta cuántos libros tienen este author_id en su lista de autores."""
        count = 0
        for data in self._books.values():
            if author_id in data['author']:
                count += 1
        return count        
    