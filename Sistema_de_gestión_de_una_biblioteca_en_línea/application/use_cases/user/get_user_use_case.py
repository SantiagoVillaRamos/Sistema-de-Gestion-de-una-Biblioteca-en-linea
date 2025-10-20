from typing import Optional
from application.ports.user_repository import UserRepository
from application.ports.loan_repository import LoanRepository
from application.ports.author_repository import AuthorRepository
from application.ports.book_repository import BookRepository
from application.dto.user_command_dto import UserDetailsDTO


class GetUserUseCase:
    
    def __init__(
        self, 
        user_repo: UserRepository, 
        loan_repo: LoanRepository, 
        book_repo: BookRepository,
    ):
        self.user_repo = user_repo
        self.loan_repo = loan_repo
        self.book_repo = book_repo

    async def execute(self, user_id: str) -> Optional[UserDetailsDTO]:
        
        user = await self.user_repo.find_by_id(user_id)
            
        active_loans = await self.loan_repo.find_active_loans_by_user(user_id)
        
        if not active_loans:
            return UserDetailsDTO(user, [], {})

        book_ids = [loan.book_id for loan in active_loans]
        books = await self.book_repo.find_by_ids(book_ids)
        books_map = {book.book_id: book for book in books}
        
        # 4. Devolver el DTO de Aplicación, conteniendo objetos de Dominio puros.
        return UserDetailsDTO(
            user=user,
            active_loans=active_loans,
            loaned_books_map=books_map
        )
    
    