
from fastapi import APIRouter, Depends, status
from application.facade.facade_library import LibraryFacade
from infrastructure.web.dependencies import get_library_facade
from infrastructure.web.models import LoanResponse, MessageResponse, LendBookCommand, ReturnBookCommand
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
    command: LendBookCommand,
    lend_use_case: Annotated[LibraryFacade, Depends(get_library_facade)]
):
    return await lend_use_case.lend_book(command)
    


@router.post(
    "/books/return", 
    status_code=status.HTTP_200_OK,
    response_model=MessageResponse
)
async def return_book(
    command: ReturnBookCommand,
    return_use_case: Annotated[LibraryFacade, Depends(get_library_facade)]
):
    await return_use_case.return_book(command)
    return MessageResponse(message="Libro devuelto exitosamente")
    
    