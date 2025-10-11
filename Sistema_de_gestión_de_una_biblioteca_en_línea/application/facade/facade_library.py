from application.ports.book_repository import BookRepository
from application.ports.user_repository import UserRepository
from application.ports.loan_repository import LoanRepository
from application.use_cases.library.lend_book_use_case import LendBookUseCase
from application.ports.notification_service import NotificationService
from application.use_cases.library.return_book_use_case import ReturnBookUseCase
from application.dto.library_command_dto import LendBookCommand, ReturnBookCommand, LendBookResponse, ReturnBookResponse


class LibraryFacade:
    
    def __init__(
        self, 
        book_repo: BookRepository, 
        user_repo: UserRepository, 
        loan_repo: LoanRepository, 
        notification_service: NotificationService
        
    ):
        
        self._lend_book_use_case = LendBookUseCase(book_repo, user_repo, loan_repo, notification_service)
        self._return_book_use_case = ReturnBookUseCase(loan_repo, book_repo, user_repo, notification_service)

    async def lend_book(self, command: LendBookCommand) -> LendBookResponse:
        return await self._lend_book_use_case.execute(command)

    async def return_book(self, command: ReturnBookCommand) -> ReturnBookResponse:
        return await self._return_book_use_case.execute(command)
        

    
