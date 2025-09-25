from application.ports.book_repository import BookRepository
from application.ports.user_repository import UserRepository
from application.ports.loan_repository import LoanRepository
from domain.services.lend_book.lend_book_use_case import LendBookUseCase
from domain.services.return_book.return_book_use_case import ReturnBookUseCase

from domain.services.lend_book.lend_book_command import LendBookCommand
from domain.services.return_book.return_book_command import ReturnBookCommand
from infrastructure.web.models import LoanResponse


class LibraryFacade:
    
    def __init__(self, book_repo: BookRepository, user_repo: UserRepository, loan_repo: LoanRepository):
        
        self._lend_book_use_case = LendBookUseCase(book_repo, user_repo, loan_repo)
        self._return_book_use_case = ReturnBookUseCase(loan_repo, book_repo)

    async def lend_book(self, command: LendBookCommand) -> LoanResponse:
        return await self._lend_book_use_case.execute(command)

    async def return_book(self, command: ReturnBookCommand) -> None:
        await self._return_book_use_case.execute(command)
        

    
