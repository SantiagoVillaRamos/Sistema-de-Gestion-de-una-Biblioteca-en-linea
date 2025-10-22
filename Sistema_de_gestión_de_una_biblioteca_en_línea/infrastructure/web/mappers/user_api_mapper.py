from infrastructure.web.model.user_models import UserResponse, GetUserResponse, CreateUserRequest, LoanResponse, UserListResponse, UserListResponseItem, UpdateUserRequest, UserLoanHistoryResponse, LoanHistoryItemResponse
from application.dto.user_command_dto import UserLoanHistoryDTO
from application.dto.user_command_dto import CreateUserCommand, UpdateUserCommand
from application.dto.user_command_dto import UserDetailsDTO
from domain.models.user import User
from domain.models.loan import Loan
from domain.models.author import Author
from domain.models.book import Book
from typing import Dict, List, Optional

class UserAPIMapper:
    
    @staticmethod
    def to_create_command(request: CreateUserRequest) -> CreateUserCommand:
        """Mapea el DTO de entrada HTTP al Comando de Creación."""
        return CreateUserCommand(
            name=request.name,
            email=request.email,
            password=request.password,
            user_type=request.user_type,
            roles=request.roles 
        )
        
    @staticmethod
    def from_entity_to_creation_response(user: User) -> UserResponse:
        """Mapea la Entidad User (con VOs) al DTO de respuesta HTTP (con strings)."""
        return UserResponse(
            user_id=user.user_id,
            name=user.name,
            email=user.email.address,
            user_type=user.user_type,
            roles=user.roles
        )
        
        
    @staticmethod
    def _map_loan_to_response(loan: Loan, book_map: Dict[str, Book], authors_map: Dict[str, Author]) -> LoanResponse:
        """Helper para mapear una entidad Loan a su DTO de respuesta, enriqueciendo con Book."""
        
        book = book_map.get(loan.book_id)
        
        book_title = "Título no disponible"
        due_date_value = None

        if loan.book_id in book_map:
            book_title = book_map[loan.book_id].title.value # <-- Extrae VO
        
        if loan.due_date is not None:
            due_date_value = loan.due_date.value # <-- Extrae VO
        
        book_authors_names = []
        if book and book.author:
            # Iteramos sobre los IDs de autor del libro (book.author)
            # y mapeamos el ID al nombre usando el authors_map
            book_authors_names = [
                authors_map[author_id].name.value # <--- Extraemos el Objeto de Valor (VO) del nombre
                for author_id in book.author
                if author_id in authors_map 
            ]   
        
             
        return LoanResponse(
            message="Préstamo activo",
            loan_id=loan.id, 
            book_title=book_title,
            description=book_map[loan.book_id].description,
            authors=book_authors_names,
            loan_date=loan.loan_date,
            due_date=due_date_value 
        )
        
        
    @staticmethod
    def from_details_dto_to_get_response(details: UserDetailsDTO) -> GetUserResponse:
        """Mapea el DTO de Aplicación enriquecido al DTO final de la API."""
        
        # 1. Mapear la lista de préstamos usando el mapa de libros
        loan_instances = [
            UserAPIMapper._map_loan_to_response(loan, details.loaned_books_map, details.loaned_authors_map)
            for loan in details.active_loans
        ]
        
        #Convertir cada instancia de DTO a un diccionario (datos brutos)
        #    para que Pydantic pueda anidarlos sin error.
        loaned_books_list_as_dicts = [
            instance.model_dump()
            for instance in loan_instances
        ]
        
        # 2. Crear el DTO final del usuario
        return GetUserResponse(
            user_id=details.user.user_id,
            name=details.user.name,
            email=details.user.email.address, # <-- Extrae VO
            is_active=details.user.is_active,
            loaned_books=loaned_books_list_as_dicts
        )    
    
    @staticmethod
    def from_entity_list_to_response(users: List[User]) -> UserListResponse:
        """Mapea una lista de entidades User al DTO UserListResponse."""
        
        user_items = []
        for user in users:
            # Reutilizamos el mapeo de los atributos básicos
            item = UserListResponseItem(
                user_id=user.user_id,
                name=user.name,
                email=user.email.address, # Extraer VO
                user_type=user.user_type,
                roles=user.roles,
                is_active=user.is_active
            )
            user_items.append(item)
            
        return UserListResponse(users=user_items)
    
    @staticmethod
    def to_update_command(request: UpdateUserRequest, user_id: str) -> UpdateUserCommand:
        """Convierte la solicitud web al comando de aplicación."""
        return UpdateUserCommand(
            user_id=user_id,
            name=request.name,
            new_email=request.email,
            new_password=request.password,
        )
        
    @staticmethod
    def from_entity_to_update_response(user: User) -> UserResponse:
        """Reutilizamos el DTO de creación, ya que muestra el estado actual del usuario."""
        
        return UserAPIMapper.from_entity_to_creation_response(user)
    

    @staticmethod
    def _map_loan_to_history_item(
        loan: Loan, 
        book_map: Dict[str, Book], 
        authors_map: Dict[str, Author]
    ) -> LoanHistoryItemResponse:
        
        book = book_map.get(loan.book_id)
        
        # Manejo de datos base del préstamo
        book_title = book.title.value if book else "Título Desconocido"
        authors_names = []
        
        if book:
            authors_names = [
                authors_map[author_id].name.value
                for author_id in book.author
                if author_id in authors_map
            ]
            
        return LoanHistoryItemResponse(
            loan_id=loan.id, 
            book_title=book_title,
            authors=authors_names,
            loan_date=loan.loan_date,
            due_date=loan.due_date.value,
            is_active=loan.is_returned
        )


    @staticmethod
    def from_loan_history_dto_to_response(history_dto: UserLoanHistoryDTO) -> UserLoanHistoryResponse:
        """Mapea el DTO de historial de préstamos al DTO de respuesta HTTP."""
        
        # 1. Mapear cada entidad Loan al DTO de respuesta
        loan_items = [
            UserAPIMapper._map_loan_to_history_item(
                loan, 
                history_dto.loaned_books_map, 
                history_dto.loaned_authors_map
            ).model_dump() # Convertir a dict para anidación Pydantic
            for loan in history_dto.loans
        ]
        
        # 2. Construir la respuesta final
        return UserLoanHistoryResponse(
            user_id=history_dto.user.user_id,
            user_name=history_dto.user.name,
            loans=loan_items
        )
