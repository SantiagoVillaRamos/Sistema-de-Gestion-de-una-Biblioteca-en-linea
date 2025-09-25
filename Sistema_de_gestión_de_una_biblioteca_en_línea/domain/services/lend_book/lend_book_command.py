from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class LendBookCommand:
    """
    DTO para los datos de entrada del caso de uso de prestar un libro.
    """
    user_id: str
    book_id: str
    
    
@dataclass(frozen=True)
class LoanResponse:
    """
    DTO para los datos de salida del caso de uso de prestar un libro.
    """
    message: str
    loan_id: str
    book_title: str
    loan_date: datetime
    due_date: datetime