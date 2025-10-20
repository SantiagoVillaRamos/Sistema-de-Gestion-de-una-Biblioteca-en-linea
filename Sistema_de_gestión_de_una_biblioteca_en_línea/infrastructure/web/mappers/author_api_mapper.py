
from infrastructure.web.model.author_dtos import CreateAuthorRequest, CreateAuthorResponse, AuthorDetailResponse
from application.dto.author_command_dto import CreateAuthorCommand
from infrastructure.web.mappers.book_mappers import BookAPIMapperResponse
from application.dto.author_command_dto import UpdateAuthorCommand
from infrastructure.web.model.author_dtos import UpdateAuthorRequest
from domain.models.author import Author
from domain.models.book import Book
from typing import List, Dict

class AuthorAPIMapper:
    
    @staticmethod
    def to_create_command(request: CreateAuthorRequest) -> CreateAuthorCommand:
        """Mapea el DTO de entrada HTTP al Comando de Aplicación."""
        return CreateAuthorCommand(name=request.name, description=request.description)

    @staticmethod
    def from_entity_to_create_response(author: Author) -> CreateAuthorResponse:
        """Mapea la Entidad Author (con VOs) al DTO de respuesta HTTP (con strings)."""
        return CreateAuthorResponse(
            author_id=author.author_id,
            name=author.name.value,         
            description=author.description.value
        )
        
    @staticmethod
    def from_entity_list_to_response_list(authors: List[Author]) -> List[CreateAuthorResponse]:
        """Mapea una lista de entidades Author a una lista de DTOs de respuesta."""
        return [
            AuthorAPIMapper.from_entity_to_create_response(author)
            for author in authors
        ]
        
    
    @staticmethod
    def from_full_details_to_response(author: Author, books: List[Book], all_authors_map: Dict[str, Author]) -> AuthorDetailResponse:
        """Mapea la tupla (Author, List[Book]) a AuthorDetailResponse."""
        
        book_instances = []
        for book in books:
            # 1. Obtener los nombres de autor para ESTE libro usando el mapa global
            book_author_names = [
                all_authors_map[author_id].name.value
                for author_id in book.author
                if author_id in all_authors_map
            ]
            # 2. Llamar al mapper del libro inyectando los nombres
            instance = BookAPIMapperResponse.from_entity_to_response(
                book, 
                author_names=book_author_names
            )
            book_instances.append(instance)
        
        # CONVERSIÓN CRÍTICA: Convertir cada instancia de DTO a un diccionario
        # antes de pasarla al constructor del DTO final.
        book_dtos_as_dicts = [
            instance.model_dump() 
            for instance in book_instances
        ]
        
        return AuthorDetailResponse(
            author_id=author.author_id,
            name=author.name.value,
            description=author.description.value,
            books=book_dtos_as_dicts
        )
        
    @staticmethod
    def to_update_command(request: UpdateAuthorRequest) -> UpdateAuthorCommand:
        """Mapea el DTO de entrada HTTP al Comando de Actualización."""
        return UpdateAuthorCommand(
            name=request.name,
            description=request.description
        )
    