from abc import ABC, abstractmethod
from application.dto.book_command_dto import BookDetailsResponse


class GetBookById(ABC):
    
    @abstractmethod
    async def get_book_by_id(self, book_id: str) -> BookDetailsResponse:
        pass