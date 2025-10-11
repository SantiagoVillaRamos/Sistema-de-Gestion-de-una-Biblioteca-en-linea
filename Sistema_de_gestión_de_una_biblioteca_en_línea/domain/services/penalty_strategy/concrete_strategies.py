from datetime import datetime
from domain.models.loan import Loan
from .penalty_strategy import PenaltyStrategy

class StudentPenaltyStrategy(PenaltyStrategy):
    """
    Estrategia de multa para estudiantes: 0.50 por día de retraso.
    """
    def calculate_penalty(self, loan: Loan) -> float:
        if not loan.is_overdue():
            return 0.0
        
        overdue_days = (datetime.now() - loan.due_date.value).days
        return overdue_days * 0.50

class ProfessorPenaltyStrategy(PenaltyStrategy):
    """
    Estrategia de multa para profesores: 0.25 por día de retraso, con 5 días de gracia.
    """
    def calculate_penalty(self, loan: Loan) -> float:
        if not loan.is_overdue():
            return 0.0
            
        overdue_days = (datetime.now() - loan.due_date.value).days
        return max(0, overdue_days - 5) * 0.25

class GeneralPublicPenaltyStrategy(PenaltyStrategy):
    """
    Estrategia de multa para público general: 1.00 por día de retraso.
    """
    def calculate_penalty(self, loan: Loan) -> float:
        if not loan.is_overdue():
            return 0.0
        
        overdue_days = (datetime.now() - loan.due_date.value).days
        return overdue_days * 1.00