from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class CreateUserCommand:
    """
    DTO para los datos de entrada del caso de uso de crear un usuario.
    """
    name: str
    email: str
    

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