from application.dto.library_command_dto import LendBookResult
from infrastructure.web.model.lend_models import LoanResponse, LoanedUserResponse, LoanedBookResponse


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

