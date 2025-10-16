from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal


class MessageResponse(BaseModel):
    
    message: str


class LoanResponse(BaseModel):
    
    message: str
    loan_id: str
    book_title: str
    description: str
    authors: List[str]
    loan_date: datetime
    due_date: datetime



class CreateUserRequest(BaseModel):
    
    name: str
    email: str
    password: str = Field(..., max_length=72)
    user_type: Literal["student", "professor", "general"]
    roles: List[str] = None
    

    
class UserCreationResponse(BaseModel):
    
    user_id: str
    name: str
    email: EmailStr
    user_type: Literal["student", "professor", "general"]
    roles: List[str]


class GetUserResponse(BaseModel):
    
    user_id: str
    name: str
    email: EmailStr
    is_active: bool
    loaned_books: List[LoanResponse] = []
    
    

class CreateAuthorRequest(BaseModel):
    
    name: str
    description: str

class CreateAuthorResponse(BaseModel):
    
    author_id: str
    name: str
    description: str
    
class LendBookRequest(BaseModel):
    
    user_id: str
    book_id: str
    
    
    
class ReturnBookRequest(BaseModel):

    loan_id: str

class ReturnBookResponse(BaseModel):
    
    message: str
    penalty_charged: float

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72)

class LoginResponse(BaseModel):
    token: str
    token_type: str = "bearer"