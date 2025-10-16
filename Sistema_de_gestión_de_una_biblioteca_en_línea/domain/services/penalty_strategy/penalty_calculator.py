from domain.models.user import User
from domain.models.loan import Loan
from domain.ports.penalty_strategy import PenaltyStrategy
from .concrete_strategies import StudentPenaltyStrategy, ProfessorPenaltyStrategy, GeneralPublicPenaltyStrategy
from domain.models.exceptions.business_exception import BusinessTypeError

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
        user_type = getattr(user, 'user_type', 'general')
        if user_type == 'student':
            return StudentPenaltyStrategy()
        elif user_type == 'professor':
            return ProfessorPenaltyStrategy()
        elif user_type == 'general':
            return GeneralPublicPenaltyStrategy()
        else:
            return BusinessTypeError(f"Tipo de usuario inválido: {user_type}")

    def calculate(self, loan: Loan) -> float:
        return self._strategy.calculate_penalty(loan)
    
