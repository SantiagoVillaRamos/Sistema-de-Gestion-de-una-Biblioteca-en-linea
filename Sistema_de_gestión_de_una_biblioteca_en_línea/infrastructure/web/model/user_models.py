from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal, Optional
from datetime import datetime


class UserResponse(BaseModel):
    
    user_id: str
    name: str
    email: EmailStr
    user_type: Literal["student", "professor", "general"]
    roles: List[str]


class CreateUserRequest(BaseModel):
    
    name: str
    email: str
    password: str = Field(..., max_length=72)
    user_type: Literal["student", "professor", "general"]
    roles: List[str] = None
    

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

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


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
    
    
# class LoanResponse(BaseModel):
#     """Modelo de respuesta para el préstamo de un libro."""
#     message: str
#     loan_id: str
#     book_title: str
#     loan_date: datetime
#     due_date: datetime