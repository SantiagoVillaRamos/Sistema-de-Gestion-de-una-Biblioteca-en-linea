from application.dto.library_command_dto import LendBookResult, LoanReportData
from infrastructure.web.model.lend_models import LoanReportItemResponse, UserResponse, BookResponse
from infrastructure.web.model.lend_models import LoanResponse, LoanedUserResponse, LoanedBookResponse
from typing import List


class LoanApiMapper:
    
    DESCRIPTION_LIMIT = 50
    
    @staticmethod
    def _truncate_description(description: str, limit: int) -> str:
        """Trunca una cadena a un límite de caracteres, añadiendo puntos suspensivos."""
        if not description or len(description) <= limit:
            return description
        
        # Corta la cadena y asegura que no corta a mitad de una palabra (opcional, pero mejor UX)
        truncated = description[:limit]
        
        # Encuentra el último espacio para evitar cortar una palabra
        last_space = truncated.rfind(' ')
        if last_space > 0:
            truncated = truncated[:last_space]
            
        return f"{truncated}..."

    @staticmethod
    def from_application_dto_to_response(app_dto: LendBookResult) -> LoanResponse:
        
        # 1. Obtenemos la descripción completa del dominio
        full_description = app_dto.book.description 
        
        # 2. Aplicamos la lógica de truncamiento
        truncated_description = LoanApiMapper._truncate_description(
            full_description, 
            LoanApiMapper.DESCRIPTION_LIMIT
        )
        
        loan = app_dto.loan
        user = app_dto.user
        book = app_dto.book
        
        # 1. Mapear datos del usuario
        user_data = LoanedUserResponse(
            user_id=user.user_id,
            name=user.name,
            email=user.email.address
        )
        
        # 2. Mapear datos del libro
        book_data = LoanedBookResponse(
            book_id=book.book_id,
            title=book.title.value,
            description=truncated_description,
            authors=app_dto.author_names
        )
        
        # 3. Mapear el modelo principal
        return LoanResponse(
            message=app_dto.message,
            loan_id=loan.id,
            loan_date=loan.loan_date,
            due_date=loan.due_date.value,
            user=user_data,
            book=book_data
        )
        
    @staticmethod
    def from_report_dto_list_to_response(data_list: List[LoanReportData]) -> List[LoanReportItemResponse]:
        """Mapea la lista de datos enriquecidos de Aplicación a la lista de DTOs de respuesta web."""
        
        # Mapeamos cada objeto LoanReportData
        return [
            LoanReportItemResponse(
                # --- Datos del Préstamo (Nivel Raíz) ---
                loan_id=item.loan.id, 
                loan_date=item.loan.loan_date,
                due_date=item.loan.due_date.value,
                is_returned=item.loan.is_returned,
                is_overdue=item.loan.is_overdue(), # Llama al método de dominio

                # --- Datos del Usuario (Objeto Anidado) ---
                user=UserResponse(
                    user_id=item.user.user_id,
                    name=item.user.name,
                    email=item.user.email.address,
                ),
                
                # --- Datos del Libro (Objeto Anidado) ---
                book=BookResponse(
                    book_id=item.book.book_id,
                    title=item.book.title.value,
                    authors=item.author_names, 
                ),
            ) for item in data_list
        ]

