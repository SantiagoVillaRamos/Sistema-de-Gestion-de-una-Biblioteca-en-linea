from application.ports.book_repository import BookRepository
from application.ports.user_repository import UserRepository
from application.ports.loan_repository import LoanRepository
from application.ports.author_repository import AuthorRepository
from application.dto.library_command_dto import LendBookCommand, LendBookResult
from application.ports.notification_service import NotificationService
from domain.services.lending_service import LendingService
from domain.models.book import Book

class LendBookUseCase:  
    
    def __init__(
        self, 
        book_repo: BookRepository, 
        user_repo: UserRepository, 
        loan_repo: LoanRepository,
        notification_service: NotificationService,
        author_repos: AuthorRepository
    ):
        self._book_repo = book_repo
        self._user_repo = user_repo
        self._loan_repo = loan_repo
        self._notification_service = notification_service
        self._author_repo = author_repos
        self._lending_service = LendingService()

    async def execute(self, command: LendBookCommand) -> LendBookResult:
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
        # 5. Preparar el resultado
        author_names = await self._get_author_names(book.author, book)
        
        return LendBookResult(
            loan=new_loan,
            user=user,
            book=book,
            author_names=author_names,
        )
        
    async def _get_author_names(self, author_ids: list[str], book:Book ) -> list[str]:
        
        author_ids = book.author
        authors = await self._author_repo.find_by_ids(author_ids)
        author_names = [author.name.value for author in authors]
        return author_names
        