from fastapi import APIRouter, Depends, status
from typing import List
from application.facade.facade_book import FacadeBook
from infrastructure.web.dependencies import get_book_facade, RoleChecker
from infrastructure.web.model.book_models import CreateBookResponse, CreateBookRequest, GetBooksResponse, UpdateBookDTO, BookMessage, BookFullResponseDTO
from typing import Annotated
from infrastructure.web.mappers.book_mappers import BookAPIMapper

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
    command = BookAPIMapper.to_create_command(request)
    new_book = await facade.create_book(command)
    return BookAPIMapper.from_entity_to_create_response(new_book)


@router.get(
    "/",
    response_model=List[GetBooksResponse]
)
async def get_all_books(
    facade: Annotated[FacadeBook, Depends(get_book_facade)]
):
    
    enriched_books = await facade.get_all_books()
    return [
        BookAPIMapper.from_enriched_dict_to_response(book)
        for book in enriched_books
    ]
    



@router.get("/{book_id}", response_model=BookFullResponseDTO)
async def get_book_details(
    book_id: str,
    facade: Annotated[FacadeBook, Depends(get_book_facade)]
):
    
    response_dto = await facade.get_book_by_id(book_id) 
    return BookAPIMapper.from_full_details_to_response(response_dto)
   
    
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
    command = BookAPIMapper.to_update_command(request)
    book, author_names = await facade.update_book(book_id, command)
    return BookAPIMapper.from_update_result_to_response(book, author_names)
    


@router.delete(
    "/{book_id}", 
    status_code=status.HTTP_200_OK,
    response_model=BookMessage,
    #dependencies=[Depends(admin_role_checker)]
)
async def delete_book(
    book_id: str,
    facade: Annotated[FacadeBook, Depends(get_book_facade)]
):
    book_deleted = await facade.delete_book(book_id)
    return BookMessage(
        message=f"Libro '{book_deleted.title.value}' Eliminado"
    )
