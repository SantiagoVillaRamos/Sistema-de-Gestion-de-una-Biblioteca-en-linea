from domain.models.exceptions.business_exception import BusinessConflictError
from application.ports.author_repository import AuthorRepository
from application.ports.book_repository import BookRepository
from domain.models.author import Author

class DeleteAuthorUseCase:
    
    def __init__(self, author_repository: AuthorRepository, book_repository: BookRepository):
        self.author_repo = author_repository
        self.book_repo = book_repository

    async def execute(self, author_id: str) -> Author:
        # 1. Cargar el Agregado Raíz (para obtener el nombre antes de eliminar)
        author_to_delete: Author = await self.author_repo.find_by_id(author_id)
        
        # 2. VERIFICACIÓN DE LÓGICA DE NEGOCIO
        await self._count_books_by_author(author_id, author_to_delete)
        await self.author_repo.delete(author_id)
        
        return author_to_delete
    
    
    async def _count_books_by_author(self, author_id: str, author_to_delete: Author) -> None:
        
        books_count = await self.book_repo.count_by_author_id(author_id)
        
        if books_count > 0:
            raise BusinessConflictError(
                author_to_delete.name.value, 
                f"El autor tiene {books_count} libros asociados y no puede ser eliminado."
            )
        
        