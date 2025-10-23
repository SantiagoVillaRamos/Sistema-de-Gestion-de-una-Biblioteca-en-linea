from domain.models.loan import Loan
from domain.models.value_objects.due_date import DueDate

class LoanMapper:
    
    @staticmethod
    def to_persistence(loan: Loan) -> dict:
        """
        Convierte un objeto de dominio Loan a un diccionario para persistencia.
        """
        return {
            "id": loan.id,
            "user_id": loan.user_id,
            "book_id": loan.book_id,
            "loan_date": loan.loan_date,
            "due_date": loan.due_date.value,
            "is_returned": loan.is_returned
        }

    @staticmethod
    def to_domain(loan_data: dict) -> Loan:
        """
        Convierte un diccionario de persistencia a un objeto de dominio Loan.
        """
        return Loan(**loan_data)