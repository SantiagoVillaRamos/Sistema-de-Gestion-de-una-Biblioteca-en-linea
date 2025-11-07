from abc import ABC, abstractmethod
from domain.models.author import Author


class DeleteAuthor(ABC):
    
    @abstractmethod
    async def delete_author(self, author_id: str) -> Author:
        pass
