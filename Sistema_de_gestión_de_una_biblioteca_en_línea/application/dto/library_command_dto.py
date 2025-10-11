from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class LendBookCommand:
    user_id: str
    book_id: str

@dataclass(frozen=True)
class ReturnBookCommand:
    loan_id: str

@dataclass(frozen=True)
class LendBookResponse:
    message: str
    loan_id: str
    book_title: str
    loan_date: datetime
    due_date: datetime

@dataclass(frozen=True)
class ReturnBookResponse:
    message: str
    penalty_charged: float