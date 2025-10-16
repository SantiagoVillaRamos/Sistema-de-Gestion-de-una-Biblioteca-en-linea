from application.ports.book_repository import BookRepository
from application.dto.book_command_dto import GetBookCommand, BookMessage
from typing import Optional

class DeleteBookUseCase:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    async def execute(self, book_id: GetBookCommand) -> Optional[BookMessage]:
        
        book = await self.book_repository.find_by_id(book_id)
        
        await self.book_repository.delete(book)
        
        return BookMessage(
            message= f"Libro '{book.title}' eliminado con exito"
        )
