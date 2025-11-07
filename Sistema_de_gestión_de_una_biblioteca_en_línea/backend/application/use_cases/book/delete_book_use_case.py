from domain.ports.book_repository import BookRepository
from domain.models.book import Book
from application.ports.book.delete_book import DeleteBook

class DeleteBookUseCase(DeleteBook):
    
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    async def delete_book(self, book_id: str) -> Book:
        
        book = await self.book_repository.find_by_id(book_id)
        await self.book_repository.delete(book)
        return book
        
