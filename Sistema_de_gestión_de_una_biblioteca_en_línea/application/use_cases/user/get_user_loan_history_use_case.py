
from typing import List, Dict, Tuple
from domain.models.user import User
from application.ports.loan_repository import LoanRepository
from application.ports.book_repository import BookRepository
from application.ports.author_repository import AuthorRepository
from application.ports.user_repository import UserRepository
from application.dto.user_command_dto import UserLoanHistoryDTO
from domain.models.loan import Loan
from domain.models.book import Book
from domain.models.author import Author




class GetUserLoanHistoryUseCase:
    
    def __init__(
        self, 
        user_repo: UserRepository, 
        loan_repo: LoanRepository, 
        book_repo: BookRepository, 
        author_repo: AuthorRepository
    ):
        self.user_repo = user_repo
        self.loan_repo = loan_repo
        self.book_repo = book_repo
        self.author_repo = author_repo

    async def execute(self, user_id: str) -> UserLoanHistoryDTO:
        
        # 1. Obtener el usuario
        user = await self.user_repo.find_by_id(user_id)
            
        # 2. Obtener TODAS las entidades Loan del usuario (Historial)
        loans = await self.loan_repo.find_all_by_user(user_id)
        
        if not loans:
            return UserLoanHistoryDTO(user, [], {}, {})
        
        # 3. Obtener los libros y autores asociados a esos préstamos
        books_map, authors_map = await self.get_books_and_authors(loans)
        
        # 4. Devolver el DTO de Aplicación enriquecido
        return UserLoanHistoryDTO(
            user=user,
            loans=loans,
            loaned_books_map=books_map,
            loaned_authors_map=authors_map
        )
        
    async def get_books_and_authors(
        self, 
        loans: List[Loan]
    ) -> Tuple[Dict[str, Book], Dict[str, Author]]:
        """Helper para obtener mapas de libros y autores dados una lista de préstamos."""
        
        book_ids = list({loan.book_id for loan in loans})
        books = await self.book_repo.find_by_ids(book_ids)
        books_map = {book.book_id: book for book in books}
        
        all_author_ids = set()
        for book in books:
            all_author_ids.update(book.author)
            
        authors = await self.author_repo.find_by_ids(list(all_author_ids))
        authors_map = {author.author_id: author for author in authors}
        
        return books_map, authors_map