from abc import ABC, abstractmethod
from domain.models.book import Book

class DeleteBook(ABC):
    
    @abstractmethod
    async def delete_book(self, book_id: str) -> Book:
        pass
    