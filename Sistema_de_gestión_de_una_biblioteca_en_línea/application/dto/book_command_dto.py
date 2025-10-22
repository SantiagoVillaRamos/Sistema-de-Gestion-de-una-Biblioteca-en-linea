from dataclasses import dataclass
from typing import List
from domain.models.book import Book
from domain.models.author import Author

@dataclass(frozen=True)
class CreateBookCommand:
    """
    DTO para los datos de entrada del caso de uso de crear un libro.
    """
    isbn: str
    title: str
    author: List[str]
    description: str
    available_copies: int
    

@dataclass(frozen=True)
class CreateBookResult:
    """Contiene la entidad Book creada y los nombres de los autores enriquecidos."""
    book: Book
    author_names: List[str]    
    

@dataclass(frozen=True)
class CreateBookResponse:
    """
    DTO para los datos de salida del caso de uso de crear un libro.
    """
    book_id: str
    isbn: str
    title: str
    author: List[str]
    description: str
    
@dataclass(frozen=True)
class GetBookCommand:
    """
    DTO para los datos de entrada del caso de uso de traer un usuario.
    """
    book_id: str
    
@dataclass(frozen=True) 
class BookDetailsResponse:
    
    book: Book
    authors: List[Author]
    
    
@dataclass(frozen=True)
class UpdateBookDTOCommand:
    
    title: str
    description: str
    

@dataclass(frozen=True)
class BookMessage:
    
    message: str