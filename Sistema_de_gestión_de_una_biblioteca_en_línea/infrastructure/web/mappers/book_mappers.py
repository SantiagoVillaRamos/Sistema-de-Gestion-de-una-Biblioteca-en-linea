from typing import List, Dict, Any
from infrastructure.web.model.book_models import CreateBookResponse, CreateBookRequest, GetBooksResponse, BookFullResponseDTO, AuthorResponseDTO, UpdateBookDTO
from application.dto.book_command_dto import CreateBookCommand, UpdateBookDTOCommand
from domain.models.book import Book 
from domain.models.author import Author


class BookAPIMapper:
    
    """
    Gestiona la conversión entre DTOs de la capa Web (Request/Response) 
    y objetos internos (Commands/Entidades).
    """
    
    # --- ENTRADA (Mapeo a Commands) ---
    @staticmethod
    def to_create_command(request: CreateBookRequest) -> CreateBookCommand:
        """Convierte CreateBookRequest a CreateBookCommand."""
        return CreateBookCommand(
            isbn=request.isbn,
            title=request.title,
            author=request.author,
            description=request.description,
            available_copies=request.available_copies
        )

    # --- SALIDA (Mapeo de Entidad a Response) ---
    
    @staticmethod
    def from_entity_to_create_response(new_book: Book) -> CreateBookResponse:
        """Convierte la Entidad Book a CreateBookResponse."""
        return CreateBookResponse(
            book_id=new_book.book_id,
            isbn=new_book.isbn.value,
            title=new_book.title.value,
            author=new_book.author, 
            description=new_book.description
        )

    @staticmethod
    def from_enriched_dict_to_response(book: Dict[str, Any]) -> GetBooksResponse:
        """Convierte el diccionario enriquecido de GetAllBooksUseCase a GetBooksResponse."""
        return GetBooksResponse(
            isbn=book['isbn'],
            title=book['title'],
            author_names=book['author_names'], 
            description=book['description'],
            available_copies=book['available_copies']
        )
        
    @staticmethod
    def from_authors_to_dto(authors: List[Author]) -> List[AuthorResponseDTO]:
        """Convierte List[Author] a List[AuthorResponseDTO]."""
        return [
            AuthorResponseDTO(
                author_id=author.author_id, 
                name=author.name, 
                description=author.description
            )
            for author in authors
        ]

    @staticmethod
    def from_full_details_to_response(response_dto: BookFullResponseDTO) -> BookFullResponseDTO:
        """Convierte la respuesta completa (Book + Authors) a BookFullResponseDTO."""
        
        # Uso del mapper interno para los autores
        authors_http_dtos = BookAPIMapper.from_authors_to_dto(response_dto.authors)
        
        return BookFullResponseDTO(
            book_id=response_dto.book.book_id,
            isbn=response_dto.book.isbn.value,
            title=response_dto.book.title.value,
            description=response_dto.book.description,
            available_copies=response_dto.book.available_copies,
            authors=authors_http_dtos
        )
    
    @staticmethod
    def to_update_command(request: UpdateBookDTO) -> UpdateBookDTOCommand:
        """Convierte UpdateBookDTO a UpdateBookDTOCommand."""
        
        return UpdateBookDTOCommand(
            title=request.title,
            description=request.description
        )
        
    @staticmethod
    def from_update_result_to_response(book: Book, author_names: List[str]) -> GetBooksResponse:
        """Convierte la tupla (Book, List[str]) del Caso de Uso a GetBooksResponse."""
        return GetBooksResponse(
            isbn=book.isbn.value,
            title=book.title.value,
            author_names=author_names,
            description=book.description,
            available_copies=book.available_copies
        )
        