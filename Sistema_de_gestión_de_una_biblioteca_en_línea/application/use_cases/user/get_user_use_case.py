from typing import Optional
from application.ports.user_repository import UserRepository
from application.ports.loan_repository import LoanRepository
from application.ports.book_repository import BookRepository
from domain.models.user import User
from application.dto.user_command_dto import GetUserCommand, GetUserResponse, LoanResponse
from typing import List


class GetUserUseCase:
    
    def __init__(self, user_repo: UserRepository, loan_repo: LoanRepository, book_repo: BookRepository):
        self.user_repo = user_repo
        self.loan_repo = loan_repo
        self.book_repo = book_repo

    async def execute(self, user_id: GetUserCommand) -> Optional[User]:
        
        user = await self.user_repo.find_by_id(user_id)
        active_loans = await self.loan_repo.find_active_loans_by_user(user_id)
        
        if not active_loans:
            return self._build_user_response(user, [])
        
        # Optimización: Obténer todos los IDs de los libros prestados en una lista
        book_ids = [loan.book_id for loan in active_loans]
        
        # buscar múltiples libros por sus IDs
        books = await self.book_repo.find_by_ids(book_ids)
        books_dict = {book.book_id: book for book in books}
        
        #lista de respuestas de préstamos
        loaned_books_list = [
            LoanResponse(
                message="Libro prestado exitosamente",
                loan_id=loan.id,
                book_title=books_dict[loan.book_id].title.value if loan.book_id in books_dict else "Título no disponible",
                loan_date=loan.loan_date,
                due_date=loan.due_date.value     
            )for loan in active_loans
        ]
        
        return self._build_user_response(user, loaned_books_list)
        
    def _build_user_response(self, user, loaned_books_list: List[LoanResponse]) -> GetUserResponse:
        return GetUserResponse(
            user_id=user.user_id,
            name=user.name,
            email=user.email.address,
            is_active=user.is_active,
            loaned_books=loaned_books_list
        )
        
        
        