from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from domain.models.value_objects.due_date import DueDate

from domain.models.exceptions.business_exception import BusinessNotFoundError, BusinessConflictError

@dataclass
class Loan:
    
    id: str 
    book_id: str
    user_id: str
    loan_date: datetime
    due_date: DueDate
    is_returned: bool = False

    def __post_init__(self):
        
        # Asegurarse de que due_date sea siempre un objeto DueDate
        if isinstance(self.due_date, datetime):
            self.due_date = DueDate(self.due_date)
            
        if not self.book_id or not self.user_id:
            raise BusinessNotFoundError(self.id ,"El ID del libro y el ID del usuario son obligatorios.")
        if self.loan_date > self.due_date.value:
            raise BusinessNotFoundError(self.loan_date ,"La fecha de préstamo no puede ser posterior a la fecha de vencimiento.")

    def return_loan(self) -> None:
        
        if self.is_returned:
            raise BusinessConflictError(self.id)
        self.is_returned = True


    def is_overdue(self) -> bool:
        return not self.is_returned and datetime.now() > self.due_date.value
    