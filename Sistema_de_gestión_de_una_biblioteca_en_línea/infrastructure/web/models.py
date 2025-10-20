
from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal
from datetime import datetime

class MessageResponse(BaseModel):
    
    message: str



class LendBookRequest(BaseModel):
    
    user_id: str
    book_id: str
    

class LoanResponse(BaseModel):
    
    message: str
    loan_id: str
    book_title: str
    description: str
    authors: List[str]
    loan_date: datetime
    due_date: datetime


    
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