from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.loan import Loan

class LoanRepository(ABC):
    """
    Interfaz para el repositorio de Préstamos.
    """
    @abstractmethod
    async def save(self, loan: Loan) -> None:
        pass
    
    @abstractmethod
    async def update(self, loan: Loan) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, loan_id: str) -> Optional[Loan]:
        pass

    @abstractmethod
    async def find_active_loans_by_user(self, user_id: str) -> List[Loan]:
        pass