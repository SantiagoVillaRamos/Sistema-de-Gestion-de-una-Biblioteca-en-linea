from abc import ABC, abstractmethod
from domain.models.author import Author
from typing import List

class GetAllAuthors(ABC):
    
    @abstractmethod
    async def get_all_authors(self) -> List[Author]:
        pass
    
    