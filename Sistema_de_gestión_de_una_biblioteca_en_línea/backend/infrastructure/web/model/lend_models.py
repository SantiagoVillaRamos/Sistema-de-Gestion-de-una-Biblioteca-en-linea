
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
    
    
class LoanReportItemResponse(BaseModel):
    loan_id: str
    loan_date: datetime
    due_date: datetime
    
    # Usuario
    user_id: str
    user_name: str
    user_email: str
    
    # Libro
    book_id: str
    book_title: str
    book_description: str
    book_authors: List[str]