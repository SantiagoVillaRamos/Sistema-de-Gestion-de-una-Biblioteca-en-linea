from application.ports.book_repository import BookRepository
from application.ports.author_repository import AuthorRepository
from domain.models.book import Book
from domain.models.author import Author
from application.dto.book_command_dto import BookDetailsResponse
from typing import List

class GetBookByIdUseCase:
    
    def __init__(self, book_repository: BookRepository, author_repository: AuthorRepository):
        self.book_repository = book_repository
        self.author_repository = author_repository

    async def execute(self, book_id: str) -> BookDetailsResponse:
        
        book: Book = await self.book_repository.find_by_id(book_id)
        
        authors: List[Author] = await self._find_authores_for_book(book)
       
        return BookDetailsResponse(
            book=book,
            authors=authors
        )
        
    async def _find_authores_for_book(self, book:Book) -> List[Author]:
        """
        Busca las entidades Author asociadas a un libro, o devuelve una lista vacía.
        """
        if not book.author:
            return []
        
        author_ids: List[str] = book.author
        
        authors = await self.author_repository.find_by_ids(author_ids)
        return authors
    
    