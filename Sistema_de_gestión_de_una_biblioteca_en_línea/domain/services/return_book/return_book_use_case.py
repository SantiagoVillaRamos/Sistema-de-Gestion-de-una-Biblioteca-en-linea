from application.ports.loan_repository import LoanRepository
from application.ports.book_repository import BookRepository

from . return_book_command import ReturnBookCommand

from domain.exceptions.loan import (
    LoanNotFoundException, 
    LoanAlreadyReturnedException
)


class ReturnBookUseCase:
    
    def __init__(
        self, 
        loan_repo: LoanRepository, 
        book_repo: BookRepository
    ):
        self.loan_repo = loan_repo
        self.book_repo = book_repo

    async def execute(self, command: ReturnBookCommand) -> str:
    
        loan = await self.loan_repo.find_by_id(command.loan_id)
        book = await self.book_repo.find_by_id(loan.book_id)
        
        if loan.is_returned:
            raise LoanAlreadyReturnedException(command.loan_id, "El préstamo ya fue devuelto anteriormente.")

        if loan.is_overdue():
            raise LoanNotFoundException(command.loan_id, "El préstamo está vencido y no puede ser devuelto.")
        
        loan.return_loan()  
        book.return_book()  

        await self.loan_repo.update(loan)
        await self.book_repo.update(book)
        
        
        
        

