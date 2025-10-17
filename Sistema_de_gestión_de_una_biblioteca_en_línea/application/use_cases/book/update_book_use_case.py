from application.ports.book_repository import BookRepository
from application.dto.book_command_dto import UpdateBookDTOCommand
from typing import Optional, List
from domain.models.book import Book
from application.ports.author_repository import AuthorRepository

class UpdateBookUseCase:
    def __init__(self, book_repository: BookRepository, author_repository: AuthorRepository):
        self.book_repository = book_repository
        self.author_repository = author_repository

    async def execute(self, book_id: str, update_dto: UpdateBookDTOCommand) -> Optional[Book]:
        
        book = await self.book_repository.find_by_id(book_id)
        update_data = update_dto.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(book, key, value)
        
        await self.book_repository.update(book)
        
        # --- ENRIQUECIMIENTO (NUEVA LÓGICA) ---
        author_ids = book.author
        
        # 1. Obtener los objetos Author completos
        authors = await self.author_repository.find_by_ids(author_ids)
        
        # 2. Extraer solo los nombres (usando list comprehension)
        author_names: List[str] = [author.name for author in authors]
        
        # 3. Devolver la entidad del libro Y la lista de nombres
        return (book, author_names)
    

