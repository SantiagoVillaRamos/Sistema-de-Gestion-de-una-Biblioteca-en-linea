from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.loan import Loan

class LoanRepository(ABC):
    """
    Define la interfaz para el repositorio de Préstamos.
    """
    @abstractmethod
    async def save(self, loan: Loan) -> None:
        """Guarda un préstamo nuevo o actualiza uno existente."""
        pass
    
    @abstractmethod
    async def update(self, loan: Loan) -> None:
        """Actualiza un préstamo existente."""
        pass

    @abstractmethod
    async def find_by_id(self, loan_id: str) -> Optional[Loan]:
        """Busca un préstamo por su ID."""
        pass

    @abstractmethod
    async def find_active_loans_by_user(self, user_id: str) -> List[Loan]:
        """Obtiene todos los préstamos activos de un usuario."""
        pass