from typing import Dict, Optional, List
from application.ports.loan_repository import LoanRepository
from domain.entities.loan import Loan
from domain.exceptions.loan import LoanAlreadyReturnedException, LoanNotFoundException

class LoanInMemoryRepository(LoanRepository):
    
    def __init__(self):
        self._loans: Dict[str, Loan] = {}

    async def save(self, loan: Loan) -> None:
        if loan.id in self._loans:
            raise LoanAlreadyReturnedException(loan.id, "El préstamo ya existe.")
        self._loans[loan.id] = loan
        
    async def update(self, loan: Loan) -> None:
        if loan.id not in self._loans:
            raise LoanNotFoundException(loan.id, "No se puede actualizar un préstamo que no existe.")
        self._loans[loan.id] = loan

    async def find_by_id(self, loan_id: str) -> Optional[Loan]:
        loan = self._loans.get(loan_id)
        if not loan:
            raise LoanNotFoundException(loan_id, "El préstamo no existe.")
        return loan
        
    async def find_active_loans_by_user(self, user_id: str) -> List[Loan]:
        return [loan for loan in self._loans.values() if loan.user_id == user_id and not loan.is_returned]