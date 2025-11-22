from domain.models.loan import Loan
from domain.models.value_objects.due_date import DueDate
from infrastructure.persistence.models import LoanModel
from typing import Optional
from datetime import datetime

class LoanMapper:
    
    @staticmethod
    def to_persistence(loan: Loan) -> dict:
        """
        Convierte un objeto de dominio Loan a un diccionario para persistencia.
        """
        return {
            "id": loan.id,
            "user_id": loan.user_id,
            "book_id": loan.book_id,
            "loan_date": loan.loan_date,
            "due_date": loan.due_date.value,
            "is_returned": loan.is_returned
        }

    @staticmethod
    def to_domain(loan_data: dict | LoanModel) -> Loan:
        """
        Convierte un diccionario de persistencia o Modelo DB a un objeto de dominio Loan.
        """
        
        if loan_data is None:
            return None
        
        if isinstance(loan_data, dict):
            # Asegurar que due_date sea DueDate si viene como datetime o string
            due_date_val = loan_data['due_date']
            if isinstance(due_date_val, str):
                try:
                    due_date_val = datetime.fromisoformat(due_date_val)
                except ValueError:
                    pass 

            return Loan(
                id=loan_data['id'],
                user_id=loan_data['user_id'],
                book_id=loan_data['book_id'],
                loan_date=loan_data['loan_date'],
                due_date=DueDate(due_date_val) if isinstance(due_date_val, datetime) else due_date_val, 
                is_returned=loan_data['is_returned']
            )
        else:
            # Es un LoanModel
            due_date_val = loan_data.due_date
            if isinstance(due_date_val, str):
                try:
                    due_date_val = datetime.fromisoformat(due_date_val)
                except ValueError:
                    pass

            return Loan(
                id=loan_data.id,
                user_id=loan_data.user_id,
                book_id=loan_data.book_id,
                loan_date=loan_data.loan_date,
                due_date=DueDate(due_date_val) if isinstance(due_date_val, datetime) else due_date_val,
                is_returned=loan_data.is_returned
            )

    @staticmethod
    def to_db_model(domain_loan: Loan, db_model: Optional[LoanModel] = None) -> LoanModel:
        """
        Convierte una Entidad de Dominio a un Modelo de DB de SQLAlchemy.
        """
        if db_model is None:
            db_model = LoanModel(id=domain_loan.id)
            
        db_model.user_id = domain_loan.user_id
        db_model.book_id = domain_loan.book_id
        db_model.loan_date = domain_loan.loan_date
        db_model.due_date = domain_loan.due_date.value
        db_model.is_returned = domain_loan.is_returned
        
        return db_model