from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid

from domain.exceptions.loan import LoanNotFoundException, LoanAlreadyReturnedException

@dataclass
class Loan:
    """
    Representa un préstamo de un libro a un usuario. Es una Entidad.
    Se define por su identidad única (ID del préstamo).
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    book_id: str
    user_id: str
    loan_date: datetime = field(default_factory=datetime.now, init=False)
    due_date: datetime = field(default_factory=lambda: datetime.now() + timedelta(days=14), init=False)
    is_returned: bool = False

    def __post_init__(self):
        
        if not self.book_id or not self.user_id:
            raise LoanNotFoundException(self.id ,"El ID del libro y el ID del usuario son obligatorios.")
        if self.loan_date > self.due_date:
            raise LoanNotFoundException(self.loan_date ,"La fecha de préstamo no puede ser posterior a la fecha de vencimiento.")

    def return_loan(self) -> None:
        """
        Marca el préstamo como devuelto.
        """
        if self.is_returned:
            raise LoanAlreadyReturnedException(self.id)
        self.is_returned = True

    def is_overdue(self) -> bool:
        """
        Verifica si el préstamo está vencido.
        """
        return not self.is_returned and datetime.now() > self.due_date
    