
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from infrastructure.security.input_validators import (
    validate_isbn,
    validate_safe_text,
    validate_description
)


class CreateBookRequest(BaseModel):
    
    isbn: str = Field(..., min_length=10, max_length=17, description="ISBN-10 or ISBN-13")
    title: str = Field(..., min_length=1, max_length=500, description="Book title")
    author: List[str] = Field(..., min_items=1, description="List of author IDs")
    description: str = Field(..., max_length=2000, description="Book description")
    available_copies: int = Field(..., ge=0, description="Number of available copies")
    
    @field_validator('isbn')
    @classmethod
    def validate_isbn_field(cls, v: str) -> str:
        """Validate ISBN format."""
        return validate_isbn(v)
    
    @field_validator('title')
    @classmethod
    def validate_title_field(cls, v: str) -> str:
        """Validate and sanitize title."""
        return validate_safe_text(v, "Title")
    
    @field_validator('description')
    @classmethod
    def validate_description_field(cls, v: str) -> str:
        """Validate and sanitize description."""
        return validate_description(v, max_length=2000)


class CreateBookResponse(BaseModel):
    
    book_id: str
    isbn: str
    title: str
    author: List[str]
    description: str
    
    
class GetBooksResponse(BaseModel):
    
    book_id: str
    isbn: str
    title: str
    author_names: List[str]
    description: str
    available_copies: int
    

class UpdateBookDTO(BaseModel):
    
    title: Optional[str] = Field(None, min_length=1, max_length=500, description="Updated title")
    description: Optional[str] = Field(None, max_length=2000, description="Updated description")
    
    @field_validator('title')
    @classmethod
    def validate_title_field(cls, v: Optional[str]) -> Optional[str]:
        """Validate and sanitize title if provided."""
        if v is None:
            return v
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return validate_safe_text(v, "Title")
    
    @field_validator('description')
    @classmethod
    def validate_description_field(cls, v: Optional[str]) -> Optional[str]:
        """Validate and sanitize description if provided."""
        if v is None:
            return v
        return validate_description(v, max_length=2000)

    
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
    
