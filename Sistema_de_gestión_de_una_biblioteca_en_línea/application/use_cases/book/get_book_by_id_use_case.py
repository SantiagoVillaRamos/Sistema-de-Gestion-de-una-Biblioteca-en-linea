from application.ports.book_repository import BookRepository
from application.ports.author_repository import AuthorRepository
from domain.models.book import Book
from application.dto.book_command_dto import GetBookCommand, BookDetailsResponse
from typing import Optional, List

class GetBookByIdUseCase:
    
    def __init__(self, book_repository: BookRepository, author_repository: AuthorRepository):
        self.book_repository = book_repository
        self.author_repository = author_repository

    async def execute(self, book_id: GetBookCommand) -> Optional[BookDetailsResponse]:
        
        book: Book = await self.book_repository.find_by_id(book_id)
        
        if not book.author:
            return BookDetailsResponse(book=book, authors=[])

        author_ids: List[str] = book.author
        
        authors = await self.author_repository.find_by_ids(author_ids)
       
        return BookDetailsResponse(
            book=book,
            authors=authors
        )