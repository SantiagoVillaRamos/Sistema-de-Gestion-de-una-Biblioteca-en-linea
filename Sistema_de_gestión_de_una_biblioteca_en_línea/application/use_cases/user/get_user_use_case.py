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
        author_repository: AuthorRepository
    ):
        self.user_repo = user_repo
        self.loan_repo = loan_repo
        self.book_repo = book_repo
        self.author_repository = author_repository

    async def execute(self, user_id: str) -> Optional[UserDetailsDTO]:
        
        user = await self.user_repo.find_by_id(user_id)
            
        active_loans = await self.loan_repo.find_active_loans_by_user(user_id)
        
        if not active_loans:
            # Devuelve mapa de autores vacío si no hay préstamos
            return UserDetailsDTO(user, [], {}, {})

        # 3. Obtener los libros asociados a los préstamos activos
        books_map, books = await self._get_books(active_loans)
        
        # 3.1 Obtener los autores asociados a los libros
        authors_map = await self._get_authors(books)
        
        # 4. Devolver el DTO de Aplicación, conteniendo objetos de Dominio puros.
        return UserDetailsDTO(
            user=user,
            active_loans=active_loans,
            loaned_books_map=books_map,
            loaned_authors_map=authors_map
        )
    
    async def _get_books( self, active_loans: list) -> dict:
        """Helper para obtener los libros dados los préstamos activos."""
        
        book_ids = [loan.book_id for loan in active_loans]
        books = await self.book_repo.find_by_ids(book_ids)
        books_map = {book.book_id: book for book in books}
        return books_map, books
    
    
    async def _get_authors(self, books: list) -> dict:
        """Helper para obtener los autores dados los libros."""
        
        author_ids = set()
        for book in books:
            author_ids.update(book.author)
        
        authors = await self.author_repository.find_by_ids(list(author_ids))
        authors_map = {author.author_id: author for author in authors}
        return authors_map