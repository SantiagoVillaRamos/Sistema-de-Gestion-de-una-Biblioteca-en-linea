from application.ports.book_repository import BookRepository
from domain.models.book import Book
from application.dto.book_command_dto import GetBookCommand, GetResponseBookCommand
from typing import Optional

class GetBookByIdUseCase:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    async def execute(self, book_id: GetBookCommand) -> Optional[GetResponseBookCommand]:
        
        return await self.book_repository.find_by_id(book_id)
