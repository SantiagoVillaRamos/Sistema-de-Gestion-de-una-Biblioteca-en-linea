from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal, Optional


class CreateBookRequest(BaseModel):
    
    isbn: str
    title: str
    author_id: List[str]
    description: str
    available_copies: int

class CreateBookResponse(BaseModel):
    
    book_id: str
    isbn: str
    title: str
    author_id: List[str]
    description: str
    
    
class GetBooksResponse(BaseModel):
    
    isbn: str
    title: str
    author_id: List[str]
    description: str
    available_copies: int
    
class UpdateBookDTO(BaseModel):
    
    title: Optional[str] = None
    description: Optional[str] = None
    
class BookMessage(BaseModel):
    
    message: str