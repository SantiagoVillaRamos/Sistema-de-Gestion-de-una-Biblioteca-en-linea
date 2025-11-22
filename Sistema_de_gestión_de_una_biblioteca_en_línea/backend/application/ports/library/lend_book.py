from abc import ABC, abstractmethod
from application.dto.library_command_dto import LendBookCommand, LendBookResult

class LendBook(ABC):
    
    @abstractmethod
    async def execute(self, command: LendBookCommand) -> LendBookResult:
        pass
    