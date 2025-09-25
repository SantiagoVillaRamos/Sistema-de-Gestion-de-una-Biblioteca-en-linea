
from application.ports.book_repository import BookRepository
from application.ports.user_repository import UserRepository
from application.ports.loan_repository import LoanRepository
from domain.entities.loan import Loan
from . lend_book_command import LendBookCommand, LoanResponse
from domain.exceptions.book import BookNotFoundError
from domain.exceptions.user import UserNotFoundError
from domain.exceptions.book import BookNotFoundError


class LendBookUseCase:  
    """
    Caso de uso para prestar un libro a un usuario.
    Orquesta la lógica de negocio.
    """
    def __init__(
        self, 
        book_repo: BookRepository, 
        user_repo: UserRepository, 
        loan_repo: LoanRepository
    ):
        self._book_repo = book_repo
        self._user_repo = user_repo
        self._loan_repo = loan_repo

    async def execute(self, command: LendBookCommand) -> str:
        
        user = await self._user_repo.find_by_id(command.user_id)
        book = await self._book_repo.find_by_id(command.book_id)
        active_loans = await self._loan_repo.find_active_loans_by_user(user.user_id)
        
        if any(loan.is_overdue() for loan in active_loans):
            raise UserNotFoundError(user.user_id, "El usuario tiene préstamos vencidos")
        
        if not book.is_available():
            raise BookNotFoundError(book.book_id, "No hay copias disponibles")
        
        book.lend()
        
        new_loan = Loan(
            book_id=book.book_id,
            user_id=user.user_id
        )

        await self._book_repo.update(book)
        await self._loan_repo.save(new_loan)

        return self._create_loan_response(new_loan, book)
            
            
    def _create_loan_response(self, new_loan: Loan, book) -> LoanResponse:
        """Crea un objeto LoanResponse a partir de un préstamo y un libro."""
        return LoanResponse(
            message="Libro prestado exitosamente",
            loan_id=new_loan.id,
            book_title=book.title.value,
            loan_date=new_loan.loan_date,
            due_date=new_loan.due_date
        )

        
              
        