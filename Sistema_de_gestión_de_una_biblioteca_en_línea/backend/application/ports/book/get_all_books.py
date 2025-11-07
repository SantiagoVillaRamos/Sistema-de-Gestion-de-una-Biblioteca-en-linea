from abc import ABC, abstractmethod
from typing import List, Dict

class GetAllBooks(ABC):
    
    @abstractmethod
    async def get_all_books(self) -> List[Dict]:
        pass
    