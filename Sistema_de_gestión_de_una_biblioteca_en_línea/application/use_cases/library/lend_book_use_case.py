from application.ports.book_repository import BookRepository
from application.ports.user_repository import UserRepository
from application.ports.loan_repository import LoanRepository
from application.dto.library_command_dto import LendBookCommand, LendBookResponse
from application.ports.notification_service import NotificationService
from domain.services.lending_service import LendingService

class LendBookUseCase:  
    
    def __init__(
        self, 
        book_repo: BookRepository, 
        user_repo: UserRepository, 
        loan_repo: LoanRepository,
        notification_service: NotificationService
    ):
        self._book_repo = book_repo
        self._user_repo = user_repo
        self._loan_repo = loan_repo
        self._notification_service = notification_service
        self._lending_service = LendingService() # El servicio de dominio es stateless

    async def execute(self, command: LendBookCommand) -> LendBookResponse:
        # 1. Orquestación: Cargar los datos desde la persistencia
        user = await self._user_repo.find_by_id(command.user_id)
        book = await self._book_repo.find_by_id(command.book_id)
        active_loans = await self._loan_repo.find_active_loans_by_user(user.user_id)
        
        # 2. Lógica de Dominio: Delegar las reglas de negocio al servicio de dominio
        new_loan = self._lending_service.lend_book(user, book, active_loans)

        # 3. Orquestación: Persistir los cambios
        await self._book_repo.update(book)
        await self._loan_repo.save(new_loan)

        # 4. Orquestación: Enviar notificación
        await self._notification_service.send_loan_notification(user, book, new_loan)

        # 5. Orquestación: Crear la respuesta para la capa de aplicación
        return LendBookResponse(
            message="Libro prestado exitosamente",
            loan_id=new_loan.id,
            book_title=book.title.value,
            description=book.description,
            authors=book.author_id,
            loan_date=new_loan.loan_date,
            due_date=new_loan.due_date.value
        )