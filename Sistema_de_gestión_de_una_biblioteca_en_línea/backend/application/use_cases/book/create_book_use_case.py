
from domain.models.author import Author
from domain.ports.book_repository import BookRepository
from domain.ports.author_repository import AuthorRepository
from application.dto.book_command_dto import CreateBookCommand, CreateBookResult
from domain.models.factory.bookFactory import BookFactory
from domain.models.exceptions.business_exception import BusinessNotFoundError
from typing import List
from application.ports.book.create_book import CreaterBook

class CreateBookUseCase(CreaterBook):
    
    def __init__(self, book_repository: BookRepository, author_repository:AuthorRepository, book_factory:BookFactory):
        self.book_repo = book_repository
        self.author_repo = author_repository
        self.book_factory = book_factory

    async def create_book(self, command: CreateBookCommand) -> CreateBookResult:
        
        authors = await self._validate_authors_exist(command.author)
        
        response_ISBN = await self.book_repo.find_by_isbn(command.isbn)
        if response_ISBN:
            raise BusinessNotFoundError(command.isbn, "El libro con este ISBN ya existe.")
        
        response_Title = await self.book_repo.find_by_title(command.title)
        if response_Title:
            raise BusinessNotFoundError(command.title, "El titulo ya existe.")
        
        new_book = self.book_factory.create(
            isbn=command.isbn,
            title=command.title,
            author=command.author,
            description=command.description,
            available_copies=command.available_copies
        )
        
        await self.book_repo.save(new_book)
        author_names = [author.name.value for author in authors]

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
    

