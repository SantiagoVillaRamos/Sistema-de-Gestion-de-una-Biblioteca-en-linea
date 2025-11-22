
from application.dto.library_command_dto import LendBookCommand, ReturnBookCommand, LendBookResult, ReturnBookResponse

from application.ports.library.get_loan_report import GetLoanReport
from application.ports.library.lend_book import LendBook
from application.ports.library.return_book import ReturnBook

class LibraryFacade:
    
    def __init__(
        self, 
        lend_book_use_case: LendBook, 
        return_book_use_case: ReturnBook, 
        get_loan_report_use_case: GetLoanReport
    ):
        
        self._lend_book_use_case = lend_book_use_case
        self._return_book_use_case = return_book_use_case
        self._get_loan_report_use_case = get_loan_report_use_case

    async def lend_book(self, command: LendBookCommand) -> LendBookResult:
        return await self._lend_book_use_case.execute(command)

    async def return_book(self, command: ReturnBookCommand) -> ReturnBookResponse:
        return await self._return_book_use_case.return_book(command)
    
    async def get_loan_report_facade(self):
        return await self._get_loan_report_use_case.execute()
        

    
