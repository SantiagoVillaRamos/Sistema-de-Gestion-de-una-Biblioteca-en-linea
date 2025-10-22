
from application.use_cases.library.lend_book_use_case import LendBookUseCase
from application.use_cases.library.return_book_use_case import ReturnBookUseCase
from application.use_cases.library.lend_book_use_case import LendBookUseCase
from application.use_cases.library.return_book_use_case import ReturnBookUseCase
from application.use_cases.library.get_loan_report_use_case import GetLoanReportUseCase
from application.dto.library_command_dto import LendBookCommand, ReturnBookCommand, LendBookResult, ReturnBookResponse


class LibraryFacade:
    
    def __init__(
        self, 
        lend_book_use_case: LendBookUseCase, 
        return_book_use_case: ReturnBookUseCase,
        get_loan_report_use_case: GetLoanReportUseCase
    ):
        
        self._lend_book_use_case = lend_book_use_case
        self._return_book_use_case = return_book_use_case
        self._get_loan_report_use_case = get_loan_report_use_case

    async def lend_book(self, command: LendBookCommand) -> LendBookResult:
        return await self._lend_book_use_case.execute(command)

    async def return_book(self, command: ReturnBookCommand) -> ReturnBookResponse:
        return await self._return_book_use_case.execute(command)
    
    async def get_loan_report_facade(self):
        return await self._get_loan_report_use_case.execute()
        

    
