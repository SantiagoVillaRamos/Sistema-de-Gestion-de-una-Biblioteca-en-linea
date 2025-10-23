from domain.models.author import Author
from domain.models.book import Book 
from typing import Dict, List
from application.ports.book_repository import BookRepository
from application.ports.author_repository import AuthorRepository
from application.dto.author_command_dto import GetAuthorDetailsResult

class GetAuthorByIdUseCase:
    
    def __init__(self, author_repository: AuthorRepository, book_repository: BookRepository):
        self.author_repo = author_repository
        self.book_repo = book_repository


    async def execute(self, author_id: str) -> GetAuthorDetailsResult: 
        
        # 1. Obtener la entidad principal
        author = await self.author_repo.find_by_id(author_id)
        # 2. Obtener las entidades relacionadas
        books = await self.book_repo.find_by_author_id(author_id)
        # 3. Obtener el mapa de TODOS los autores relacionados (para enriquecer nombres)
        all_authors_map = await self._get_related_authors_map(books)
        
        return GetAuthorDetailsResult(
            author=author,
            books=books,
            all_authors_map=all_authors_map
        )
    
    
    async def _get_related_authors_map(self, books: List[Book]) -> Dict[str, Author]:
        """Obtiene un mapa de todas las entidades Author necesarias para enriquecer los libros."""
        
        all_book_author_ids = set()
        for book in books:
            all_book_author_ids.update(book.author)
            
        all_authors = await self.author_repo.find_by_ids(list(all_book_author_ids))
        
        # Devuelve el mapa directamente
        return {a.author_id: a for a in all_authors}
    
    