from domain.models.book import Book
from domain.models.user import User
from domain.models.loan import Loan
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass(frozen=True)
class LendBookCommand:
    user_id: str
    book_id: str

@dataclass(frozen=True)
class ReturnBookCommand:
    loan_id: str


@dataclass(frozen=True)
class LendBookResult:
    """Contiene las entidades de Dominio afectadas por el préstamo."""
    loan: Loan
    user: User
    book: Book
    author_names: List[str]
    message: str = "Libro prestado exitosamente"


@dataclass(frozen=True)
class ReturnBookResponse:
    message: str
    penalty_charged: float
   

@dataclass(frozen=True)
class LoanReportData:
    """Estructura intermedia que contiene todos los Agregados cargados por un préstamo."""
    loan: Loan
    user: User
    book: Book
    author_names: List[str] 
    
