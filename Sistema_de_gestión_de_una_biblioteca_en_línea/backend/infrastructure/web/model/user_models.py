from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Literal, Optional
from datetime import datetime
from infrastructure.security.input_validators import validate_name, validate_safe_text


class UserResponse(BaseModel):
    
    user_id: str
    name: str
    email: EmailStr
    user_type: Literal["student", "professor", "general"]
    roles: List[str]


class CreateUserRequest(BaseModel):
    
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, max_length=72, description="Strong password")
    user_type: Literal["student", "professor", "general"]
    roles: List[str] = None
    
    @field_validator('name')
    @classmethod
    def validate_name_field(cls, v: str) -> str:
        """Validate and sanitize name to prevent XSS and injection attacks."""
        return validate_name(v, min_length=2, max_length=100)
    

class UserListResponseItem(BaseModel):
    
    user_id: str
    name: str
    email: str
    user_type: str
    roles: List[str]
    is_active: bool


class UserListResponse(BaseModel):
    users: List[UserListResponseItem]


class UpdateUserRequest(BaseModel):

    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Updated name")
    email: Optional[EmailStr] = Field(None, description="Updated email address")
    password: Optional[str] = Field(None, min_length=8, max_length=72, description="New password")
    current_password: Optional[str] = Field(None, description="Current password for verification")

    @field_validator('name')
    @classmethod
    def validate_name_field(cls, v: Optional[str]) -> Optional[str]:
        """Validate and sanitize name if provided."""
        if v is None:
            return v
        # Reject empty strings
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return validate_name(v, min_length=2, max_length=100)


class LoanHistoryItemResponse(BaseModel):
    """Detalle enriquecido de un préstamo."""
    loan_id: str
    book_title: str
    authors: List[str] 
    loan_date: datetime
    due_date: datetime
    is_active: bool
    
class UserLoanHistoryResponse(BaseModel):
    user_id: str
    user_name: str
    loans: List[LoanHistoryItemResponse]

    
class LoanResponse(BaseModel):
    
    message: str
    loan_id: str
    book_title: str
    description: str
    authors: List[str]
    loan_date: datetime
    due_date: datetime

    
    
class GetUserResponse(BaseModel):
    
    user_id: str
    name: str
    email: EmailStr
    is_active: bool
    loaned_books: List[LoanResponse] = []
    
    
