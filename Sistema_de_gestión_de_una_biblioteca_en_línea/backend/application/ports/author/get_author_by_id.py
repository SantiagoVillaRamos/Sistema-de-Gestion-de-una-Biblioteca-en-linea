from abc import ABC, abstractmethod
from application.dto.author_command_dto import GetAuthorDetailsResult


class GetAuthorByID(ABC):
    
    @abstractmethod
    async def get_author_by_id(self, author_id: str) -> GetAuthorDetailsResult: 
        pass