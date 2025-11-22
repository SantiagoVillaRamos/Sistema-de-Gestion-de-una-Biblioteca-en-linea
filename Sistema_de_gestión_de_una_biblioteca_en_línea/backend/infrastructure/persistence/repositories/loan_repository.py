from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from infrastructure.persistence.models import LoanModel
from infrastructure.mapper_infrastructure.loan_mapper import LoanMapper
from domain.ports.loan_repository import LoanRepository
from domain.models.loan import Loan
from domain.models.exceptions.business_exception import BusinessError

class SQLAlchemyLoanRepository(LoanRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, loan: Loan) -> None:
        db_loan = await self.session.get(LoanModel, loan.id)
        db_loan_mapper = LoanMapper.to_db_model(loan, db_loan)
        
        if not await self.session.get(LoanModel, loan.id):
            self.session.add(db_loan_mapper)
            
        try:
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise BusinessError(f"Error saving loan: {e}")

    async def update(self, loan: Loan) -> None:
        await self.save(loan)

    async def find_by_id(self, loan_id: str) -> Optional[Loan]:
        db_loan = await self.session.get(LoanModel, loan_id)
        return LoanMapper.to_domain(db_loan)

    async def find_active_loans_by_user(self, user_id: str) -> List[Loan]:
        stmt = select(LoanModel).where(LoanModel.user_id == user_id, LoanModel.is_returned == False)
        result = await self.session.execute(stmt)
        db_loans = result.scalars().all()
        return [LoanMapper.to_domain(l) for l in db_loans]

    async def find_all_by_user(self, user_id: str) -> List[Loan]:
        stmt = select(LoanModel).where(LoanModel.user_id == user_id)
        result = await self.session.execute(stmt)
        db_loans = result.scalars().all()
        return [LoanMapper.to_domain(l) for l in db_loans]

    async def find_all(self) -> List[Loan]:
        stmt = select(LoanModel)
        result = await self.session.execute(stmt)
        db_loans = result.scalars().all()
        return [LoanMapper.to_domain(l) for l in db_loans]
