from domain.models.author import Author
from domain.models.book import Book 
from typing import Tuple, List
from application.ports.book_repository import BookRepository
from application.ports.author_repository import AuthorRepository

class GetAuthorByIdUseCase:
    
    def __init__(self, author_repository: AuthorRepository, book_repository: BookRepository):
        self.author_repo = author_repository
        self.book_repo = book_repository


    async def execute(self, author_id: str) -> Tuple[Author, List[Book]]: 
        
        author = await self.author_repo.find_by_id(author_id)
        
        books = await self.book_repo.find_by_author_id(author_id)
        
        all_book_author_ids = await self._all_book_author_ids(books)
        
        return (author, books, all_book_author_ids)
    
    
    async def _all_book_author_ids(self, books: List[Book]) -> List[str]:
        # 1. Recolectar todos los IDs de autores únicos de ESTOS libros
        all_book_author_ids = set()
        for book in books:
            all_book_author_ids.update(book.author)
        # 2. Consultar TODOS esos autores en una llamada
        all_authors = await self.author_repo.find_by_ids(list(all_book_author_ids))
        # 3. Crear un mapa global para búsqueda O(1)
        author_map = {a.author_id: a for a in all_authors}
        
        return author_map