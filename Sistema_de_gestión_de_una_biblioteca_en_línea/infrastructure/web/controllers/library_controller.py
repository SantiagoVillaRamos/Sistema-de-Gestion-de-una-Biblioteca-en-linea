
from fastapi import APIRouter, Depends, status
from application.facade.facade_library import LibraryFacade
from infrastructure.web.dependencies import get_library_facade
from infrastructure.web.models import LoanResponse, ReturnBookResponse, LendBookRequest, ReturnBookRequest
from application.dto.library_command_dto import LendBookCommand, ReturnBookCommand
from typing import Annotated


router = APIRouter(
    prefix="/library",
    tags=["Library"]
)


@router.post(
    "/books/lend", 
    status_code=status.HTTP_201_CREATED,
    response_model=LoanResponse
)
async def lend_book(
    request: LendBookRequest,
    facade: Annotated[LibraryFacade, Depends(get_library_facade)]
):
    # Traducir el modelo de la petición web (Request) al DTO de la aplicación (Command)
    command = LendBookCommand(user_id=request.user_id, book_id=request.book_id)
    return await facade.lend_book(command)



@router.post(
    "/books/return", 
    status_code=status.HTTP_200_OK,
    response_model=ReturnBookResponse
)
async def return_book(
    request: ReturnBookRequest,
    facade: Annotated[LibraryFacade, Depends(get_library_facade)]
):
    # Traducir el modelo de la petición web (Request) al DTO de la aplicación (Command)
    command = ReturnBookCommand(loan_id=request.loan_id)
    return await facade.return_book(command)