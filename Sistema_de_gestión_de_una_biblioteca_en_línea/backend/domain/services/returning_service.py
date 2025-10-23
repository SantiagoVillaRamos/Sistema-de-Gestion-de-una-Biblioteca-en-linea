from domain.models.book import Book
from domain.models.loan import Loan
from domain.models.user import User
from domain.models.exceptions.business_exception import BusinessConflictError
from domain.services.penalty_strategy.penalty_calculator import PenaltyCalculator

class ReturningService:
    """
    Servicio de Dominio que encapsula la lógica de negocio para devolver un libro.
    Opera exclusivamente con objetos de dominio.
    """

    def return_book(self, user: User, loan: Loan, book: Book) -> float:
        """
        Ejecuta las validaciones de negocio y, si son exitosas,
        modifica el estado del préstamo, del libro y calcula la multa.
        Retorna el monto de la multa calculada.
        """
        if loan.is_returned:
            raise BusinessConflictError(loan.id, "El préstamo ya fue devuelto anteriormente.")

        penalty = 0.0
        if loan.is_overdue():
            # Usamos el patrón Strategy para calcular la multa
            calculator = PenaltyCalculator(user)
            penalty = calculator.calculate(loan)
        
        loan.return_loan()  
        book.return_book()
        
        return penalty