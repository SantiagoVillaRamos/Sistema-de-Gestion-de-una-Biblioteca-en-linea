from application.ports.loan_repository import LoanRepository
from application.ports.book_repository import BookRepository
from application.ports.user_repository import UserRepository
from application.ports.notification_service import NotificationService
from application.dto.library_command_dto import ReturnBookCommand, ReturnBookResponse
from domain.services.returning_service import ReturningService


class ReturnBookUseCase:
    """
    Caso de Uso para devolver un libro. Orquesta el proceso de carga,
    validación de dominio y persistencia.
    """
    
    def __init__(
        self, 
        loan_repo: LoanRepository, 
        book_repo: BookRepository,
        user_repo: UserRepository,
        notification_service: NotificationService
    ):
        self._loan_repo = loan_repo
        self._book_repo = book_repo
        self._user_repo = user_repo
        self._notification_service = notification_service
        self._returning_service = ReturningService()

    async def execute(self, command: ReturnBookCommand) -> ReturnBookResponse:
        # 1. Orquestación: Cargar los datos desde la persistencia
        loan = await self._loan_repo.find_by_id(command.loan_id)
        book = await self._book_repo.find_by_id(loan.book_id)
        user = await self._user_repo.find_by_id(loan.user_id)
        
        # 2. Lógica de Dominio: Delegar las reglas de negocio al servicio de dominio
        penalty = self._returning_service.return_book(user, loan, book)
        
        # 3. Orquestación: Persistir los cambios
        await self._loan_repo.update(loan)
        await self._book_repo.update(book)

        # 4. Orquestación: Enviar notificación
        await self._notification_service.send_return_notification(user, book)
        
        # 5. Orquestación: Enviar notificación de multa si aplica
        if penalty > 0:
            await self._notification_service.send_penalty_notification(user, book, penalty)
        
        return ReturnBookResponse(
            message="Libro devuelto exitosamente.",
            penalty_charged=penalty
        )
