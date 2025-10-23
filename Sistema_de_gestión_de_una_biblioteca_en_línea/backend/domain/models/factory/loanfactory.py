from datetime import datetime, timedelta
from domain.models.loan import Loan
from domain.models.value_objects.due_date import DueDate
import uuid


class LoanFactory:
    
    DEFAULT_DUE_DAYS = 14 
    
    @staticmethod
    def create_loan(book_id: str, user_id: str) -> Loan:
        
        loan_id = str(uuid.uuid4())
        loan_date = datetime.now()
        due_date = DueDate(loan_date + timedelta(days=LoanFactory.DEFAULT_DUE_DAYS))
        
        return Loan(
            id=loan_id,
            book_id=book_id,
            user_id=user_id,
            loan_date=loan_date,
            due_date=due_date
        )