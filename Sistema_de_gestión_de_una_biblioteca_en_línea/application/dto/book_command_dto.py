from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class CreateBookCommand:
    """
    DTO para los datos de entrada del caso de uso de crear un libro.
    """
    isbn: str
    title: str
    author_id: List[str]
    description: str
    available_copies: int

@dataclass(frozen=True)
class CreateBookResponse:
    """
    DTO para los datos de salida del caso de uso de crear un libro.
    """
    book_id: str
    isbn: str
    title: str
    author_id: List[str]
    description: str
    
@dataclass(frozen=True)
class GetBookCommand:
    """
    DTO para los datos de entrada del caso de uso de traer un usuario.
    """
    book_id: str
    
@dataclass(frozen=True) 
class GetResponseBookCommand:
    
    isbn: str
    title: str
    author_id: List[str]
    description: str
    available_copies: int
    
@dataclass(frozen=True)
class UpdateBookDTOCommand:
    
    title: str
    description: str
    

@dataclass(frozen=True)
class BookMessage:
    
    message: str