from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import List


class MessageResponse(BaseModel):
    
    message: str


class LoanResponse(BaseModel):
    
    message: str
    loan_id: str
    book_title: str
    loan_date: datetime
    due_date: datetime



class CreateUserRequest(BaseModel):
    
    name: str
    email: str
    password: str
    user_type: str = "general"

    
class UserCreationResponse(BaseModel):
    
    user_id: str
    name: str
    email: EmailStr



class GetUserResponse(BaseModel):
    
    user_id: str
    name: str
    email: EmailStr
    is_active: bool
    loaned_books: List[LoanResponse] = []
    
    
class CreateBookRequest(BaseModel):
    
    isbn: str
    title: str
    author: str
    available_copies: int
    
class CreateBookResponse(BaseModel):
    
    book_id: str
    isbn: str
    title: str
    author: str
    
    
class LendBookRequest(BaseModel):
    
    user_id: str
    book_id: str
    
    
    
class ReturnBookRequest(BaseModel):

    loan_id: str

class ReturnBookResponse(BaseModel):
    
    message: str
    penalty_charged: float