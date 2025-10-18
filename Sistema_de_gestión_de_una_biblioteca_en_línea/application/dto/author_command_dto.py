from dataclasses import dataclass
from typing import List
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
class AuthorDetailResponse:
    author_id: str
    name: str
    description: str
    books: List[GetBooksResponse]