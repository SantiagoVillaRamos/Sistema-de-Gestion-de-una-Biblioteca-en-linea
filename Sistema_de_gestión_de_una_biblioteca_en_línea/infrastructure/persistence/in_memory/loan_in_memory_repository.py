from typing import Dict, Optional, List
from application.ports.loan_repository import LoanRepository
from domain.models.loan import Loan
from domain.models.exceptions.business_exception import BusinessConflictError, BusinessNotFoundError
from infrastructure.mapper_infrastructure.loan_mapper import LoanMapper

class LoanInMemoryRepository(LoanRepository):
    
    def __init__(self):
        self._loans: Dict[str, dict] = {}

    async def save(self, loan: Loan) -> None:
        if loan.id in self._loans:
            raise BusinessConflictError(loan.id, "El préstamo ya existe.")
        persistence_data = LoanMapper.to_persistence(loan)
        self._loans[loan.id] = persistence_data
        
    async def update(self, loan: Loan) -> None:
        if loan.id not in self._loans:
            raise BusinessNotFoundError(loan.id, "No se puede actualizar un préstamo que no existe.")
        persistence_data = LoanMapper.to_persistence(loan)
        self._loans[loan.id] = persistence_data

    async def find_by_id(self, loan_id: str) -> Optional[Loan]:
        persistence_data = self._loans.get(loan_id)
        if not persistence_data:
            raise BusinessNotFoundError(loan_id, "El préstamo no existe.")
        return LoanMapper.to_domain(persistence_data)
        
    async def find_active_loans_by_user(self, user_id: str) -> List[Loan]:
        active_loans_data = [data for data in self._loans.values() if data['user_id'] == user_id and not data['is_returned']]
        return [LoanMapper.to_domain(data) for data in active_loans_data]