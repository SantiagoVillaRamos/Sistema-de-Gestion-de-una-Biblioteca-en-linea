from abc import ABC, abstractmethod
from domain.models.author import Author
from application.dto.author_command_dto import CreateAuthorCommand

class CreateAuthor(ABC):
    
    @abstractmethod
    async def create_author(self, command: CreateAuthorCommand) -> Author:
        pass