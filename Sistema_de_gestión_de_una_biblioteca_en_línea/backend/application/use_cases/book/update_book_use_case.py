from application.ports.book_repository import BookRepository
from application.dto.book_command_dto import UpdateBookDTOCommand, UpdateBookResult
from typing import Optional, List, Dict
from domain.models.book import Book
from domain.models.value_objects.title import Title
from application.ports.author_repository import AuthorRepository
from dataclasses import asdict

_VO_MAPPING: Dict[str, type] = {
    'title': Title 
}


class UpdateBookUseCase:
    
    def __init__(self, book_repository: BookRepository, author_repository: AuthorRepository):
        self.book_repository = book_repository
        self.author_repository = author_repository

    async def execute(self, book_id: str, update_dto: UpdateBookDTOCommand) -> Optional[UpdateBookResult]:
        #1. Obtener la entidad
        book = await self.book_repository.find_by_id(book_id)
        
        #2. Aplicar la logica de actualizacion
        self._apply_updates(book, update_dto)
        
        # 3. Persistir el cambio
        await self.book_repository.update(book)
        
        #4. Enriquecer y devolver el resultado
        author_name = await self._get_author_names(book.author)
        
        return UpdateBookResult(
            book=book,
            author_names=author_name
        )
        
        
    def _apply_updates(self, book:Book, update_dto: UpdateBookDTOCommand) -> None:
        """Convierte el DTO, filtra Nones y aplica la actualización al Objeto de Dominio."""
        
        update_data = asdict(update_dto)
        update_data_filtered = {k: v for k, v in update_data.items() if v is not None}
        
        for key, value in update_data_filtered.items():
            if key in _VO_MAPPING:
                VO_Constructor = _VO_MAPPING[key]
                value = VO_Constructor(value)
            setattr(book, key, value)

    async def _get_author_names(self, author_ids: List[str]) -> List[str]:
        """Consulta el repositorio y extrae la lista de nombres de autor."""
        
        if not author_ids:
            return []
        
        # 1. Obtener los objetos Author completos
        authors = await self.author_repository.find_by_ids(author_ids)
        
        # 2. Extraer solo los nombres (usando list comprehension)
        return [author.name for author in authors]
    