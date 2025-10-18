from fastapi import APIRouter, Depends, status
from typing import List
from application.facade.facade_book import FacadeBook
from infrastructure.web.dependencies import get_book_facade, RoleChecker
from infrastructure.web.model.book_models import CreateBookResponse, CreateBookRequest, GetBooksResponse, UpdateBookDTO, BookMessage, BookFullResponseDTO, AuthorResponseDTO
from application.dto.book_command_dto import CreateBookCommand, UpdateBookDTOCommand
from domain.models.book import Book 
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
    
    # command = CreateBookCommand(
    #     isbn=request.isbn,
    #     title=request.title,
    #     author=request.author,
    #     description=request.description,
    #     available_copies=request.available_copies
    # )
    # new_book = await facade.create_book(command)
    # return CreateBookResponse(
    #     book_id=new_book.book_id,
    #     isbn=new_book.isbn.value,
    #     title=new_book.title.value,
    #     author= new_book.author, 
    #     description=new_book.description
    # )



@router.get(
    "/",
    response_model=List[GetBooksResponse]
)
async def get_all_books(
    facade: Annotated[FacadeBook, Depends(get_book_facade)]
):
    enriched_books = await facade.get_all_books()
    return [
        GetBooksResponse(
            isbn=book['isbn'],
            title=book['title'],
            author_names=book['author_names'], 
            description=book['description'],
            available_copies=book['available_copies']
        ) for book in enriched_books
    ]



@router.get("/{book_id}", response_model=BookFullResponseDTO)
async def get_book_details(
    book_id: str,
    facade: Annotated[FacadeBook, Depends(get_book_facade)]
):
    
    response_dto = await facade.get_book_by_id(book_id) 
    
    authors_http_dtos = [
        AuthorResponseDTO(
            author_id=author.author_id, 
            name=author.name, 
            description=author.description
        )
        for author in response_dto.authors
    ]
    
    return BookFullResponseDTO(
        book_id=response_dto.book.book_id,
        isbn=response_dto.book.isbn.value,
        title=response_dto.book.title.value,
        description=response_dto.book.description,
        available_copies=response_dto.book.available_copies,
        authors=authors_http_dtos 
    )
    

"""Pendiente verificar porque el ID no lo encuentra en la DB, no la lee da error"""
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
    command = UpdateBookDTOCommand(
        title=request.title,
        description=request.description
    )
    
    book, author_names = await facade.update_book(book_id, command)
    return GetBooksResponse(
        isbn=book.isbn.value,
        title=book.title.value,
        author_names=author_names,
        description=book.description,
        available_copies=book.available_copies
    )
    


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
    await facade.delete_book(book_id)
    return BookMessage(
        message=f"Libro Eliminado"
    )
