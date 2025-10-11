from typing import List
from domain.models.book import Book
from domain.models.loan import Loan
from domain.models.user import User
from domain.models.exceptions.business_exception import BusinessConflictError
from domain.models.factory.loanfactory import LoanFactory

class LendingService:
    """
    Servicio de Dominio que encapsula la lógica de negocio para prestar un libro.
    Opera exclusivamente con objetos de dominio.
    """

    def lend_book(self, user: User, book: Book, active_loans: List[Loan]) -> Loan:
        """
        Ejecuta las validaciones de negocio y, si son exitosas,
        modifica el estado del libro y crea un nuevo préstamo.
        """
        if any(loan.is_overdue() for loan in active_loans):
            raise BusinessConflictError(user.user_id, "El usuario tiene préstamos vencidos y no puede solicitar más libros.")
        
        if not book.is_available():
            raise BusinessConflictError(book.book_id, "No hay copias disponibles de este libro.")
        
        book.lend()
        
        new_loan = LoanFactory.create_loan(book.book_id, user.user_id)
        return new_loan