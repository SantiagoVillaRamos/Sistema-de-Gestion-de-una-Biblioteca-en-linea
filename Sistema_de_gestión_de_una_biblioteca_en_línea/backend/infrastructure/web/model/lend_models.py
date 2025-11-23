
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
import re


class LoanedUserResponse(BaseModel):
    user_id: str
    name: str
    email: str

class LoanedBookResponse(BaseModel):
    book_id: str
    title: str
    description: str
    authors: List[str]

class LoanResponse(BaseModel):
    
    message: str
    loan_id: str
    loan_date: datetime
    due_date: datetime
    user: LoanedUserResponse
    book: LoanedBookResponse


class LendBookRequest(BaseModel):
    """
    Request model for lending a book.
    
    🔒 SECURITY: UUID validation to prevent injection attacks.
    """
    user_id: str = Field(..., min_length=36, max_length=36, description="User UUID")
    book_id: str = Field(..., min_length=36, max_length=36, description="Book UUID")
    
    @field_validator('user_id', 'book_id')
    @classmethod
    def validate_uuid_format(cls, v: str) -> str:
        """Validate that the ID is a valid UUID format."""
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        if not re.match(uuid_pattern, v.lower()):
            raise ValueError(f'Invalid UUID format: {v}')
        return v

    
class ReturnBookRequest(BaseModel):
    """
    Request model for returning a book.
    
    🔒 SECURITY: UUID validation to prevent injection attacks.
    """
    loan_id: str = Field(..., min_length=36, max_length=36, description="Loan UUID")
    
    @field_validator('loan_id')
    @classmethod
    def validate_uuid_format(cls, v: str) -> str:
        """Validate that the ID is a valid UUID format."""
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        if not re.match(uuid_pattern, v.lower()):
            raise ValueError(f'Invalid UUID format: {v}')
        return v

class ReturnBookResponse(BaseModel):
    
    message: str
    penalty_charged: float
    
    
    
    
class UserResponse(BaseModel):
    """DTO para representar la información del usuario en el reporte."""
    user_id: str
    name: str
    email: str 

class BookResponse(BaseModel):
    """DTO para representar la información del libro en el reporte."""
    book_id: str
    title: str
    authors: List[str]
    
class LoanReportItemResponse(BaseModel):
    """DTO Principal para un ítem del reporte de préstamos."""
    
    loan_id: str
    loan_date: datetime
    due_date: datetime
    is_returned: bool
    is_overdue: bool 

    # Entidades relacionadas (anidadas)
    user: UserResponse
    book: BookResponse