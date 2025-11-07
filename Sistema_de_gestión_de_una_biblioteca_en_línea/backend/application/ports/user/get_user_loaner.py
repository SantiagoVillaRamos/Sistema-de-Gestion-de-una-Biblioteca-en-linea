from abc import ABC, abstractmethod
from application.dto.user_command_dto import UserLoanHistoryDTO


class GetUserLoaner(ABC):
    
    @abstractmethod
    async def get_user_loan(self, user_id: str) -> UserLoanHistoryDTO:
        pass


