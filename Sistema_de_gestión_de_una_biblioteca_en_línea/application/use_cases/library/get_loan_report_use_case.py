from typing import List, Dict
from application.ports.loan_repository import LoanRepository
from application.ports.user_repository import UserRepository
from application.ports.book_repository import BookRepository
from application.ports.author_repository import AuthorRepository
from application.dto.library_command_dto import LoanReportData
from domain.models.loan import Loan
from domain.models.user import User
from domain.models.book import Book
from domain.models.author import Author

class GetLoanReportUseCase:
    """Caso de uso para generar un informe de todos los préstamos con sus datos relacionados."""
    
    def __init__(
        self, 
        loan_repo: LoanRepository,
        user_repo: UserRepository,
        book_repo: BookRepository,
        author_repo: AuthorRepository
    ):
        self._loan_repo = loan_repo
        self._user_repo = user_repo
        self._book_repo = book_repo
        self._author_repo = author_repo

    async def execute(self) -> List[LoanReportData]:
        """Genera un informe de todos los préstamos con sus datos relacionados."""
        all_loans = await self._get_all_loans()
        user_map, book_map, author_map = await self._load_related_data(all_loans)
        return self._assemble_report_data(all_loans, user_map, book_map, author_map)


    async def _get_all_loans(self) -> List[Loan]:
        return await self._loan_repo.find_all()


    async def _load_related_data(self, all_loans: List[Loan]) -> tuple[Dict[str, User], Dict[str, Book], Dict[str, Author]]:
        """Carga los usuarios, libros y autores relacionados con los préstamos dados."""
        user_ids = list({loan.user_id for loan in all_loans})
        book_ids = list({loan.book_id for loan in all_loans})

        users: List[User] = await self._user_repo.find_by_ids(user_ids)
        books: List[Book] = await self._book_repo.find_by_ids(book_ids)

        user_map: Dict[str, User] = {user.user_id: user for user in users}
        book_map: Dict[str, Book] = {book.book_id: book for book in books}

        all_author_ids = list({author_id for book in books for author_id in book.author})
        authors: List[Author] = await self._author_repo.find_by_ids(all_author_ids)
        author_map: Dict[str, Author] = {author.author_id: author for author in authors}

        return user_map, book_map, author_map


    def _assemble_report_data( self, all_loans: List[Loan], user_map: Dict[str, User], book_map: Dict[str, Book], author_map: Dict[str, Author]) -> List[LoanReportData]:
        """Ensambla los datos del informe de préstamos combinando préstamos, usuarios, libros y autores."""
        report_data_list: List[LoanReportData] = []
        for loan in all_loans:
            user = user_map.get(loan.user_id)
            book = book_map.get(loan.book_id)

            if not user or not book:
                continue

            # Obtener los nombres de autores
            author_names = [author_map[aid].name.value for aid in book.author if aid in author_map]
                
            # Devolver el DTO intermedio
            report_data_list.append(LoanReportData(
                loan=loan,
                user=user,
                book=book,
                author_names=author_names
            ))
            
        return report_data_list
        
        