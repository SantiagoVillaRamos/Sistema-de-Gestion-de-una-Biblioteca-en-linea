
from domain.models.book import Book
from application.ports.book_repository import BookRepository
from application.ports.author_repository import AuthorRepository
from application.dto.book_command_dto import CreateBookCommand
from domain.models.factory.bookFactory import BookFactory
from domain.models.exceptions.business_exception import BusinessNotFoundError 
import asyncio
from typing import List

class CreateBookUseCase:
    
    def __init__(self, book_repository: BookRepository, author_repository:AuthorRepository):
        self.book_repo = book_repository
        self.author_repo = author_repository

    async def execute(self, command: CreateBookCommand) -> Book:
        
        await self._validate_authors_exist(command.author)
        
        new_book = BookFactory.create(
            isbn=command.isbn,
            title=command.title,
            author=command.author,
            description=command.description,
            available_copies=command.available_copies
        )
        
        await self.book_repo.save(new_book)

        return new_book
    
    
    async def _validate_authors_exist(self, author_ids: List[str]) -> None:
        """Valida la existencia de todos los autores de forma concurrente."""
        
        # 1. Crear una lista de tareas (consultas al repositorio)
        author_tasks = [self.author_repo.find_by_id(author_id) for author_id in author_ids]
        
        # 2. Ejecutar todas las tareas en paralelo. Retorna una lista de resultados (Author | None).
        results = await asyncio.gather(*author_tasks, return_exceptions=True)
        
        # 3. Usamos list comprehension para identificar los IDs que fallaron.
        non_existent_authors = [
            author_id 
            for author_id, result in zip(author_ids, results)
            # Verificamos si el resultado fue una instancia de tu excepción
            if isinstance(result, BusinessNotFoundError) 
        ]
        
        if non_existent_authors:
            # Construimos un mensaje consolidado de todos los errores.
            ids_str = ", ".join(non_existent_authors)
            
            # Lanzamos una única excepción con la información de todos los IDs.
            raise BusinessNotFoundError(
                ids_str,  # business_id: la lista de IDs que fallaron
                f"No se pudieron encontrar los siguientes IDs de autor: {ids_str}."
            )
    
        