
from pydantic import BaseModel
from typing import List, Optional

class CreateBookRequest(BaseModel):
    
    isbn: str
    title: str
    author: List[str]
    description: str
    available_copies: int

class CreateBookResponse(BaseModel):
    
    book_id: str
    isbn: str
    title: str
    author: List[str]
    description: str
    
    
class GetBooksResponse(BaseModel):
    
    isbn: str
    title: str
    author_names: List[str]
    description: str
    available_copies: int
    
class UpdateBookDTO(BaseModel):
    
    title: Optional[str] = None
    description: Optional[str] = None
    
class BookMessage(BaseModel):
    
    message: str
    
    
class AuthorResponseDTO(BaseModel):
    
    author_id: str
    name: str
    description: str

class BookFullResponseDTO(BaseModel):
    book_id: str
    isbn: str
    title: str
    description: str
    available_copies: int
    authors: List[AuthorResponseDTO]
    
