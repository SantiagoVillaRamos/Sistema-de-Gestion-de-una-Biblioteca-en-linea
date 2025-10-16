from application.ports.book_repository import BookRepository
from application.dto.book_command_dto import UpdateBookDTOCommand, GetResponseBookCommand
from typing import Optional


class UpdateBookUseCase:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    async def execute(self, book_id: str, update_dto: UpdateBookDTOCommand) -> Optional[GetResponseBookCommand]:
        
        book = await self.book_repository.find_by_id(book_id)
        update_data = update_dto.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(book, key, value)
        
        await self.book_repository.update(book)
        
        return self._get_updated_data_book(book)
    
    def _get_updated_data_book(self, update_data) -> GetResponseBookCommand:
        
        return GetResponseBookCommand(
            isbn=update_data.isbn,
            title=update_data.title,
            author_id=update_data.author_id,
            description=update_data.description,
            available_copies=update_data.avaliable_copies
        )
