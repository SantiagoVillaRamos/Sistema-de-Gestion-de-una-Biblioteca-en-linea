from application.ports.book_repository import BookRepository
from application.use_cases.book.create_book_use_case import CreateBookUseCase
from application.dto.book_command_dto import CreateBookCommand, CreateBookResponse

class BookFacade:
    
    def __init__(self, book_repo: BookRepository):
        self._create_book_use_case = CreateBookUseCase(book_repo)

    async def create_book_facade(self, command: CreateBookCommand) -> CreateBookResponse:
        return await self._create_book_use_case.execute(command)