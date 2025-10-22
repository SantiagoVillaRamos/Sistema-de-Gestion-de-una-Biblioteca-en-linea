from application.dto.library_command_dto import LendBookResult, LoanReportData
from infrastructure.web.model.lend_models import LoanReportItemResponse
from infrastructure.web.model.lend_models import LoanResponse, LoanedUserResponse, LoanedBookResponse
from typing import List, Dict


class LoanApiMapper:

    @staticmethod
    def from_application_dto_to_response(app_dto: LendBookResult) -> LoanResponse:
        
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
            description=book.description,
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
                # Datos del Préstamo (Loan)
                loan_id=item.loan.id, 
                loan_date=item.loan.loan_date,
                due_date=item.loan.due_date.value,
                
                # Datos del Usuario (User)
                user_id=item.user.user_id,
                user_name=item.user.name,
                user_email=item.user.email.address,
                
                # Datos del Libro (Book)
                book_id=item.book.book_id,
                book_title=item.book.title.value,
                book_description=item.book.description,
                book_authors=item.author_names, # Usamos la lista de nombres ya enriquecida
            ) for item in data_list
        ]

