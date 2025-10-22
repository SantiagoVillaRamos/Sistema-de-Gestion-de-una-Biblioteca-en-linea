
from infrastructure.web.model.author_dtos import CreateAuthorRequest, CreateAuthorResponse, AuthorDetailResponse
from application.dto.author_command_dto import CreateAuthorCommand
from infrastructure.web.mappers.book_mappers import BookAPIMapperResponse
from application.dto.author_command_dto import UpdateAuthorCommand, GetAuthorDetailsResult
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
    def from_details_result_to_response(result: GetAuthorDetailsResult) -> AuthorDetailResponse:
        
        author = result.author
        books = result.books
        all_authors_map = result.all_authors_map
        
        # 1. Mapear la lista de libros
        book_instances = []
        for book in books:
            # Enriquecer los nombres usando el mapa
            book_author_names = [
                all_authors_map[author_id].name.value
                for author_id in book.author
                if author_id in all_authors_map
            ]
            
            # Llamar a un mapper auxiliar (si existe) o construir el DTO directamente
            book_dto = BookAPIMapperResponse.from_entity_and_names(book, book_author_names)
            book_instances.append(book_dto)
            
        # 2. Construir la respuesta final.
        return AuthorDetailResponse(
            author_id=author.author_id,
            name=author.name.value,
            description=author.description.value,
            books=book_instances 
        )
        
    @staticmethod
    def to_update_command(request: UpdateAuthorRequest) -> UpdateAuthorCommand:
        """Mapea el DTO de entrada HTTP al Comando de Actualización."""
        return UpdateAuthorCommand(
            name=request.name,
            description=request.description
        )
    