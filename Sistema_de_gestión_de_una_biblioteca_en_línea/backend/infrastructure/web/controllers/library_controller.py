
from fastapi import APIRouter, Depends, status, Request
from application.facade.facade_library import LibraryFacade
from infrastructure.web.dependencie import get_library_facade, RoleChecker
from infrastructure.web.model.lend_models import LoanResponse, ReturnBookResponse, LendBookRequest, ReturnBookRequest, LoanReportItemResponse
from application.dto.library_command_dto import LendBookCommand, ReturnBookCommand
from infrastructure.web.mappers.loan_api_mapper import LoanApiMapper
from typing import Annotated, List
from slowapi import Limiter
from slowapi.util import get_remote_address


admin_role_checker = RoleChecker(["ADMIN"])

# 🔒 SECURITY: Initialize rate limiter for this router
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    tags=["Library"]
)


@router.post(
    "/lend", 
    status_code=status.HTTP_201_CREATED,
    response_model=LoanResponse,
    dependencies=[Depends(admin_role_checker)]
)
@limiter.limit("20/minute")  # 🔒 SECURITY: Prevent loan abuse
async def lend_book(
    http_request: Request,
    request: LendBookRequest,
    facade: Annotated[LibraryFacade, Depends(get_library_facade)]
):
    """
    Lend a book to a user (admin only).
    
    🔒 SECURITY: Rate limited to prevent loan abuse.
    """
    command = LendBookCommand(user_id=request.user_id, book_id=request.book_id)
    app_dto = await facade.lend_book(command)
    return LoanApiMapper.from_application_dto_to_response(app_dto)



@router.post(
    "/return", 
    status_code=status.HTTP_200_OK,
    response_model=ReturnBookResponse,
    dependencies=[Depends(admin_role_checker)]
)
@limiter.limit("20/minute")  # 🔒 SECURITY: Return operations
async def return_book(
    request: Request,
    return_request: ReturnBookRequest,
    facade: Annotated[LibraryFacade, Depends(get_library_facade)]
):
    """
    Return a borrowed book (admin only).
    
    🔒 SECURITY: Rate limited for return operations.
    """
    command = ReturnBookCommand(loan_id=return_request.loan_id)
    return await facade.return_book(command)


@router.get(
    "/report", 
    status_code=status.HTTP_200_OK,
    response_model=List[LoanReportItemResponse], 
    dependencies=[Depends(admin_role_checker)]
)
@limiter.limit("30/minute")  # 🔒 SECURITY: Report generation is expensive
async def get_loan_report(
    request: Request,
    facade: Annotated[LibraryFacade, Depends(get_library_facade)],
):
    """
    Get loan report (admin only).
    
    🔒 SECURITY: Rate limited as report generation is database-intensive.
    """
    report_dtos = await facade.get_loan_report_facade()
    return LoanApiMapper.from_report_dto_list_to_response(report_dtos)
