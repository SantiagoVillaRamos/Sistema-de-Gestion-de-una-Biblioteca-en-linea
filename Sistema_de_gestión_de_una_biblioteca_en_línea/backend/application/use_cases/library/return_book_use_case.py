from domain.ports.loan_repository import LoanRepository
from domain.ports.book_repository import BookRepository
from domain.ports.user_repository import UserRepository
from domain.ports.notification_service import NotificationService
from application.dto.library_command_dto import ReturnBookCommand, ReturnBookResponse
from domain.services.returning_service import ReturningService
from application.ports.library.return_book import ReturnBook
from domain.models.exceptions.business_exception import BusinessNotFoundError

class ReturnBookUseCase(ReturnBook):
    """
    Caso de Uso para devolver un libro. Orquesta el proceso de carga,
    validación de dominio y persistencia.
    """
    
    def __init__(
        self, 
        loan_repo: LoanRepository, 
        book_repo: BookRepository,
        user_repo: UserRepository,
        notification_service: NotificationService,
        returning_service: ReturningService
    ):
        self._loan_repo = loan_repo
        self._book_repo = book_repo
        self._user_repo = user_repo
        self._notification_service = notification_service
        self._returning_service = returning_service

    async def return_book(self, command: ReturnBookCommand) -> ReturnBookResponse:
    
        loan = await self._loan_repo.find_by_id(command.loan_id)
        if not loan:
            raise BusinessNotFoundError(command.loan_id, "El  ID no existe.")
        
        book = await self._book_repo.find_by_id(loan.book_id)
        user = await self._user_repo.find_by_id(loan.user_id)
        
        # Lógica de Dominio: Delegar las reglas de negocio al servicio de dominio
        penalty = self._returning_service.return_book(user, loan, book)
        
        # Orquestación: Persistir los cambios
        await self._loan_repo.update(loan)
        await self._book_repo.update(book)

        # Orquestación: Enviar notificación
        await self._notification_service.send_return_notification(user, book)
        
        # Orquestación: Enviar notificación de multa si aplica
        if penalty > 0:
            await self._notification_service.send_penalty_notification(user, book, penalty)
        
        return ReturnBookResponse(
            message="Libro devuelto exitosamente.",
            penalty_charged=penalty
        )

