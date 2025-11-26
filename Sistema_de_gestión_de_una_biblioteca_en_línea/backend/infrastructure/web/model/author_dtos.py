from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from infrastructure.security.input_validators import (
    validate_name,
    validate_description
)


class CreateAuthorRequest(BaseModel):
  
    name: str = Field(..., min_length=2, max_length=200, description="Author's full name")
    description: str = Field(..., max_length=2000, description="Author biography/description")
    
    @field_validator('name')
    @classmethod
    def validate_name_field(cls, v: str) -> str:
        """Validate and sanitize author name."""
        return validate_name(v, min_length=2, max_length=200)
    
    @field_validator('description')
    @classmethod
    def validate_description_field(cls, v: str) -> str:
        """Validate and sanitize description."""
        return validate_description(v, max_length=2000)


class CreateAuthorResponse(BaseModel):
   
    author_id: str
    name: str
    description: str


class GetBooksResponse(BaseModel):
    book_id: str
    isbn: str
    title: str
    author_names: List[str]
    description: str
    available_copies: int


class AuthorDetailResponse(BaseModel):
    
    author_id: str
    name: str
    description: str
    books: List[GetBooksResponse]
    

class UpdateAuthorRequest(BaseModel):
    
    name: Optional[str] = Field(None, min_length=2, max_length=200, description="Updated name")
    description: Optional[str] = Field(None, max_length=2000, description="Updated description")
    
    @field_validator('name')
    @classmethod
    def validate_name_field(cls, v: Optional[str]) -> Optional[str]:
        """Validate and sanitize name if provided."""
        if v is None:
            return v
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return validate_name(v, min_length=2, max_length=200)
    
    @field_validator('description')
    @classmethod
    def validate_description_field(cls, v: Optional[str]) -> Optional[str]:
        """Validate and sanitize description if provided."""
        if v is None:
            return v
        return validate_description(v, max_length=2000)
    
    
class AuthorMessage(BaseModel):
    message: str