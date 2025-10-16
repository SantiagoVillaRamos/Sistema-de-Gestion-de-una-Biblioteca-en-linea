from typing import List
from application.ports.book_repository import BookRepository
from domain.models.book import Book

class GetAllBooksUseCase:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    async def execute(self) -> List[Book]:
        return await self.book_repository.get_all()
