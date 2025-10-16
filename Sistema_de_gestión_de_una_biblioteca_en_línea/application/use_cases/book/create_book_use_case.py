
from domain.models.book import Book
from application.ports.book_repository import BookRepository
from application.dto.book_command_dto import CreateBookCommand, CreateBookResponse
from domain.models.factory.bookFactory import BookFactory

class CreateBookUseCase:
    
    def __init__(self, book_repository: BookRepository):
        self.book_repo = book_repository

    async def execute(self, command: CreateBookCommand) -> CreateBookResponse:
        
        new_book = BookFactory.create(
            isbn=command.isbn,
            title=command.title,
            author_id=command.author_id,
            description=command.description,
            available_copies=command.available_copies
        )
        
        await self.book_repo.save(new_book)

        return self._build_book_response(new_book)
    
    def _build_book_response(self, new_book: Book) -> CreateBookResponse:   
        
        return CreateBookResponse(
            book_id=new_book.book_id,
            isbn=new_book.isbn.value,
            title=new_book.title.value,
            author_id=new_book.author_id,
            description=new_book.description
        )
        
        