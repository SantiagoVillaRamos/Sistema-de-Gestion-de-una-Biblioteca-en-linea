from domain.models.user import User
from domain.models.loan import Loan
from .penalty_strategy import PenaltyStrategy
from .concrete_strategies import StudentPenaltyStrategy, ProfessorPenaltyStrategy, GeneralPublicPenaltyStrategy

class PenaltyCalculator:
    """
    El Contexto define la interfaz de interés para los clientes. Mantiene una
    referencia a una de las estrategias y delega el trabajo a ella.
    """
    def __init__(self, user: User):
        self._strategy = self._get_strategy(user)

    def _get_strategy(self, user: User) -> PenaltyStrategy:
        # Aquí asumimos que el objeto User tiene un atributo 'user_type'
        # Necesitarás añadir este atributo a tu modelo de dominio User.
        if getattr(user, 'user_type', 'general') == 'student':
            return StudentPenaltyStrategy()
        elif getattr(user, 'user_type', 'general') == 'professor':
            return ProfessorPenaltyStrategy()
        else:
            return GeneralPublicPenaltyStrategy()

    def calculate(self, loan: Loan) -> float:
        return self._strategy.calculate_penalty(loan)
    
