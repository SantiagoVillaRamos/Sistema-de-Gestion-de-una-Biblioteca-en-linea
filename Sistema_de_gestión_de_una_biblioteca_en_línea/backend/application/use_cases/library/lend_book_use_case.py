from domain.ports.book_repository import BookRepository
from domain.ports.user_repository import UserRepository
from domain.ports.loan_repository import LoanRepository
from domain.ports.author_repository import AuthorRepository
from application.dto.library_command_dto import LendBookCommand, LendBookResult
from domain.ports.notification_service import NotificationService
from domain.services.lending_service import LendingService
from domain.models.book import Book
from application.ports.library.lend_book import LendBook
from domain.models.exceptions.business_exception import BusinessNotFoundError


class LendBookUseCase(LendBook):  
    
    def __init__(
        self, 
        book_repo: BookRepository, 
        user_repo: UserRepository, 
        loan_repo: LoanRepository,
        notification_service: NotificationService,
        author_repos: AuthorRepository,
        lending_service: LendingService
    ):
        self._book_repo = book_repo
        self._user_repo = user_repo
        self._loan_repo = loan_repo
        self._notification_service = notification_service
        self._author_repo = author_repos
        self._lending_service = lending_service

    async def lend_book(self, command: LendBookCommand) -> LendBookResult:
        
        # Orquestación: Cargar los datos desde la persistencia
        user = await self._user_repo.find_by_id(command.user_id)
        if not user:
            raise BusinessNotFoundError(command.user_id, "El ID no existe.")
        
        book = await self._book_repo.find_by_id(command.book_id)
        if not book:
            raise BusinessNotFoundError(command.book_id, "El ID no existe.")
        
        active_loans = await self._loan_repo.find_active_loans_by_user(user.user_id)
        
        #Lógica de Dominio: Delegar las reglas de negocio al servicio de dominio
        new_loan = self._lending_service.lend_book(user, book, active_loans)

        #Persistir los cambios
        await self._book_repo.update(book)
        await self._loan_repo.save(new_loan)

        # Enviar notificación
        await self._notification_service.send_loan_notification(user, book, new_loan)
        # Preparar el resultado
        author_names = await self._get_author_names(book.author)
        
        return LendBookResult(
            loan=new_loan,
            user=user,
            book=book,
            author_names=author_names,
        )
        
    async def _get_author_names(self, author_ids: list[str]) -> list[str]:
        
        response_authors_ids = await self._author_repo.find_by_ids(author_ids)
        author_names = [author.name.value for author in response_authors_ids]
        return author_names
        