
from fastapi import APIRouter, Depends, status
from application.facade.facade_library import LibraryFacade
from infrastructure.web.dependencie import get_library_facade, RoleChecker
from infrastructure.web.model.lend_models import LoanResponse, ReturnBookResponse, LendBookRequest, ReturnBookRequest, LoanReportItemResponse
from application.dto.library_command_dto import LendBookCommand, ReturnBookCommand
from infrastructure.web.mappers.loan_api_mapper import LoanApiMapper
from typing import Annotated, List


admin_role_checker = RoleChecker(["ADMIN"])

router = APIRouter(
    tags=["Library"]
)


@router.post(
    "/lend", 
    status_code=status.HTTP_201_CREATED,
    response_model=LoanResponse,
    dependencies=[Depends(admin_role_checker)]
)
async def lend_book(
    request: LendBookRequest,
    facade: Annotated[LibraryFacade, Depends(get_library_facade)]
):
    command = LendBookCommand(user_id=request.user_id, book_id=request.book_id)
    app_dto = await facade.lend_book(command)
    return LoanApiMapper.from_application_dto_to_response(app_dto)



@router.post(
    "/return", 
    status_code=status.HTTP_200_OK,
    response_model=ReturnBookResponse,
    dependencies=[Depends(admin_role_checker)]
)
async def return_book(
    request: ReturnBookRequest,
    facade: Annotated[LibraryFacade, Depends(get_library_facade)]
):
    command = ReturnBookCommand(loan_id=request.loan_id)
    return await facade.return_book(command)


@router.get(
    "/report", 
    status_code=status.HTTP_200_OK,
    response_model=List[LoanReportItemResponse], 
    dependencies=[Depends(admin_role_checker)]
)
async def get_loan_report(
    facade: Annotated[LibraryFacade, Depends(get_library_facade)],
):
    report_dtos = await facade.get_loan_report_facade()
    return LoanApiMapper.from_report_dto_list_to_response(report_dtos)