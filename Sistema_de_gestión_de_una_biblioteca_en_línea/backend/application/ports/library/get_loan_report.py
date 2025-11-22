from abc import ABC, abstractmethod
from typing import List
from application.dto.library_command_dto import LoanReportData


class GetLoanReport(ABC):
    
    @abstractmethod
    async def execute(self) -> List[LoanReportData]:
        pass