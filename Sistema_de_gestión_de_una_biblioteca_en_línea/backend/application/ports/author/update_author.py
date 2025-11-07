from abc import ABC, abstractmethod
from domain.models.author import Author
from application.dto.author_command_dto import UpdateAuthorCommand

class UpdateAuthor(ABC):
    
    @abstractmethod
    async def update_author(self, author_id: str, command: UpdateAuthorCommand) -> Author:
        pass

