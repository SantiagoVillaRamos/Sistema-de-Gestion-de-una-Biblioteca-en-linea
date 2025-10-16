from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from application.facade.facade_book import FacadeBook
from infrastructure.web.dependencies import get_book_facade, RoleChecker
from infrastructure.web.model.book_models import CreateBookResponse, CreateBookRequest, GetBooksResponse, UpdateBookDTO, BookMessage
from application.dto.book_command_dto import CreateBookCommand, GetBookCommand, UpdateBookDTOCommand
from domain.models.book import Book  # Assuming Book model can be used as a response model
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
    #dependencies=[Depends(admin_role_checker)]
)
async def add_book(
    request: CreateBookRequest,
    facade: Annotated[FacadeBook, Depends(get_book_facade)]
):
    command = CreateBookCommand(
        isbn=request.isbn,
        title=request.title,
        author_id=request.author_id,
        description=request.description,
        available_copies=request.available_copies
    )
    return await facade.create_book(command)


@router.get(
    "/",
    response_model=List[GetBooksResponse]
)
async def get_all_books(
    facade: Annotated[FacadeBook, Depends(get_book_facade)]
):
    return await facade.get_all_books()


@router.get(
    "/{book_id}", 
    response_model=GetBooksResponse
)
async def get_book_by_id(
    book_id: str,
    facade: Annotated[FacadeBook, Depends(get_book_facade)]
):
    command = GetBookCommand(book_id=book_id)
    return await facade.get_book_by_id(command)
    


@router.put(
    "/{book_id}", 
    response_model=GetBooksResponse,
    #dependencies=[Depends(admin_role_checker)]
)
async def update_book(
    book_id: str,
    request: UpdateBookDTO,
    facade: Annotated[FacadeBook, Depends(get_book_facade)]
):
    command_id = GetBookCommand(book_id=book_id)
    command = UpdateBookDTOCommand(
        title=request.title,
        description=request.description
    )
    return await facade.update_book(command_id, command)
    


@router.delete(
    "/{book_id}", 
    #status_code=status.HTTP_204_NO_CONTENT,
    response_model=BookMessage,
    #dependencies=[Depends(admin_role_checker)]
)
async def delete_book(
    book_id: str,
    facade: Annotated[FacadeBook, Depends(get_book_facade)]
):
    command = GetBookCommand(book_id=book_id)
    return await facade.delete_book(command)
    
