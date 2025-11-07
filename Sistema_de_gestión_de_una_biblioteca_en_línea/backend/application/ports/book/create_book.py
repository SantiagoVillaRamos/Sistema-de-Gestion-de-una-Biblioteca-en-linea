from abc import ABC, abstractmethod
from application.dto.book_command_dto import CreateBookCommand, CreateBookResult

class CreaterBook(ABC):
    
    @abstractmethod
    async def create_book(self, command: CreateBookCommand) -> CreateBookResult:
        pass
