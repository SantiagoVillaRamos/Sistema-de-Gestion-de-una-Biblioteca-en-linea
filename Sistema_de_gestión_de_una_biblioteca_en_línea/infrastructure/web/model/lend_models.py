
from pydantic import BaseModel
from typing import List
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
    
    # Datos del préstamo
    loan_id: str
    loan_date: datetime
    due_date: datetime
    
    # Datos enriquecidos (Sub-modelos)
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