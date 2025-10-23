from abc import ABC, abstractmethod
from domain.models.loan import Loan

class PenaltyStrategy(ABC):
    """
    La interfaz Strategy declara operaciones comunes a todas las versiones
    soportadas de un algoritmo. El contexto utiliza esta interfaz para llamar
    al algoritmo definido por las estrategias concretas.
    """
    @abstractmethod
    def calculate_penalty(self, loan: Loan) -> float:
        pass