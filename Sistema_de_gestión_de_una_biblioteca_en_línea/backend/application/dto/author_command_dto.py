from dataclasses import dataclass
from typing import List, Optional, Dict
from domain.models.author import Author
from domain.models.book import Book

@dataclass(frozen=True)
class CreateAuthorCommand:
    """
    DTO para los datos de entrada del caso de uso de crear un autor.
    """
    name: str
    description: str

@dataclass(frozen=True)
class CreateAuthorResponse:
    """
    DTO para los datos de salida del caso de uso de crear un autor.
    """
    author_id: str
    name: str
    description: str

@dataclass(frozen=True)
class GetBooksResponse:
    
    isbn: str
    title: str
    author: List[str]
    description: str
    available_copies: int

@dataclass(frozen=True)
class UpdateAuthorCommand:
    
    name: Optional[str] = None
    description: Optional[str] = None
    
    
@dataclass(frozen=True)
class GetAuthorDetailsResult:
    """Resultado enriquecido del caso de uso GetAuthorById."""
    author: Author
    books: List[Book]
    all_authors_map: Dict[str, Author]
    