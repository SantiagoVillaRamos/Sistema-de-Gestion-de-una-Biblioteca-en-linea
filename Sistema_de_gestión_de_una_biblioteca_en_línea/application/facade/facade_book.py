from application.ports.book_repository import BookRepository
from application.ports.user_repository import UserRepository
from application.ports.loan_repository import LoanRepository
from application.use_cases.book.create_book_use_case import CreateBookUseCase
from application.dto.book_command_dto import CreateBookCommand


class BookFacade:
    
    def __init__(self, book_repo: BookRepository, user_repo: UserRepository, loan_repo: LoanRepository):
        self._create_book_use_case = CreateBookUseCase(book_repo)
        
    async def create_book_facade(self, command: CreateBookCommand) -> str:
        return await self._create_book_use_case.execute(command)
    
    
