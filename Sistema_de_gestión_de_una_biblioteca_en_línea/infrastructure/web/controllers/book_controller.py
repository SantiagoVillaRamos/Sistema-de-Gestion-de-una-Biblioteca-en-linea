from fastapi import APIRouter, Depends, status

from application.facade.facade_book import BookFacade
from infrastructure.web.dependencies import get_book_facade, RoleChecker
from infrastructure.web.models import CreateBookRequest, CreateBookResponse
from application.dto.book_command_dto import CreateBookCommand
from typing import Annotated


admin_role_checker = RoleChecker(["ADMIN"])

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=CreateBookResponse,
    dependencies=[Depends(admin_role_checker)]
)
async def add_book(
    request: CreateBookRequest,
    facade: Annotated[BookFacade, Depends(get_book_facade)]
):
    # Traducir el modelo de la petición web (Request) al DTO de la aplicación (Command)
    command = CreateBookCommand(
        isbn=request.isbn,
        title=request.title,
        author=request.author,
        available_copies=request.available_copies
    )
    return await facade.create_book_facade(command)
    
