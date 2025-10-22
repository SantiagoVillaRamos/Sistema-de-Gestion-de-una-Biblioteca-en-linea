
from domain.models.author import Author
from application.ports.book_repository import BookRepository
from application.ports.author_repository import AuthorRepository
from application.dto.book_command_dto import CreateBookCommand, CreateBookResult
from domain.models.factory.bookFactory import BookFactory
from domain.models.exceptions.business_exception import BusinessNotFoundError 
from typing import List

class CreateBookUseCase:
    
    def __init__(self, book_repository: BookRepository, author_repository:AuthorRepository):
        self.book_repo = book_repository
        self.author_repo = author_repository

    async def execute(self, command: CreateBookCommand) -> CreateBookResult:
        
        authors = await self._validate_authors_exist(command.author)
        
        new_book = BookFactory.create(
            isbn=command.isbn,
            title=command.title,
            author=command.author,
            description=command.description,
            available_copies=command.available_copies
        )
        
        await self.book_repo.save(new_book)
        author_names = self._extract_author_names(authors)

        return CreateBookResult(
            book=new_book,
            author_names=author_names
        )
    
    
    async def _validate_authors_exist(self, author_ids: List[str]) -> List[Author]:
        """Valida la existencia de todos los autores de forma concurrente."""
        
        # 1. Crear una lista de tareas (consultas al repositorio)
        authors: List[Author] = await self.author_repo.find_by_ids(author_ids)
        
        if len(authors) != len(author_ids):
            # Identificar cuáles IDs faltan
            found_ids = {author.author_id for author in authors}
            non_existent_ids = [id for id in author_ids if id not in found_ids]
            
            ids_str = ", ".join(non_existent_ids)
            raise BusinessNotFoundError(
                ids_str, 
                f"No se pudieron encontrar los siguientes IDs de autor: {ids_str}."
            )
            
        return authors
    
    def _extract_author_names(self, authors: List[Author]) -> List[str]:
        """Extrae los nombres de los autores de la lista de autores."""
        return [author.name.value for author in authors]

