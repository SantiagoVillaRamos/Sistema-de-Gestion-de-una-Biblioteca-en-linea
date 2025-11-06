
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


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
    
    user_id: str
    book_id: str
    

    
class ReturnBookRequest(BaseModel):

    loan_id: str

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