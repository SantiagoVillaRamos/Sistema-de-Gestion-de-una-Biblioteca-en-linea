from abc import ABC, abstractmethod
from application.dto.library_command_dto import ReturnBookCommand, ReturnBookResponse

class ReturnBook(ABC):
    
    @abstractmethod
    async def return_book(self, command: ReturnBookCommand) -> ReturnBookResponse:
        pass