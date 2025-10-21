from dataclasses import dataclass
from typing import Dict
from domain.models.user import User
from domain.models.loan import Loan
from domain.models.author import Author
from datetime import datetime
from typing import Literal, List

@dataclass(frozen=True)
class CreateUserCommand:
    """
    DTO para los datos de entrada del caso de uso de crear un usuario.
    """
    name: str
    email: str
    password: str
    user_type: Literal["student", "professor", "general"] = "general"
    roles: List[str] = None
    

@dataclass(frozen=True)
class UserDetailsDTO:
    """DTO para transportar detalles del usuario junto con sus préstamos activos y libros prestados."""
    user: User
    active_loans: List[Loan]
    loaned_books_map: Dict[str, Author]
    loaned_authors_map: Dict[str, Author]
    
    

@dataclass(frozen=True)
class LoanResponse:
    """Modelo de respuesta para el préstamo de un libro."""
    message: str
    loan_id: str
    book_title: str
    loan_date: datetime
    due_date: datetime
    

@dataclass(frozen=True)
class CreateUserResponse:
    """
    DTO para los datos de salida del caso de uso de crear un usuario.
    """
    user_id: str
    name: str
    email: str
    user_type: Literal["student", "professor", "general"]
    roles: List[str]
    
    
@dataclass(frozen=True)
class GetUserCommand:
    """
    DTO para los datos de entrada del caso de uso de traer un usuario.
    """
    user_id: str
    
    
@dataclass(frozen=True)
class GetUserResponse:
    """
    DTO para los datos de salida del caso de uso de traer un usuario.
    """
    user_id: str
    name: str
    email: str
    is_active: bool
    loaned_books: list[LoanResponse] = None


@dataclass(frozen=True)
class LoginUserCommand:
    """
    DTO para los datos de entrada del caso de uso de login de usuario.
    """
    email: str
    password: str


@dataclass(frozen=True)
class LoginUserResponse:
    """
    DTO para los datos de salida del caso de uso de login de usuario.
    """
    token: str