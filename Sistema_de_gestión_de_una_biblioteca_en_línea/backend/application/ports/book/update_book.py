from abc import ABC, abstractmethod
from application.dto.book_command_dto import UpdateBookDTOCommand, UpdateBookResult
from typing import Optional

class UpdateBook(ABC):
    
    @abstractmethod
    async def update_book(self, book_id: str, update_dto: UpdateBookDTOCommand) -> Optional[UpdateBookResult]:
        pass