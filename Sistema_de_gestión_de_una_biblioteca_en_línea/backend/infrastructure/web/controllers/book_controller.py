from fastapi import APIRouter, Depends, status, Request
from typing import List
from application.facade.facade_book import FacadeBook
from infrastructure.web.dependencie import get_book_facade, RoleChecker
from infrastructure.web.model.book_models import CreateBookResponse, CreateBookRequest, GetBooksResponse, UpdateBookDTO, BookMessage, BookFullResponseDTO
from typing import Annotated
from infrastructure.web.mappers.book_mappers import BookAPIMapper
from slowapi import Limiter
from slowapi.util import get_remote_address

admin_role_checker = RoleChecker(["ADMIN"])

# 🔒 SECURITY: Initialize rate limiter for this router
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    tags=["Books"]
)


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=CreateBookResponse,
    dependencies=[Depends(admin_role_checker)]
)
@limiter.limit("30/minute")  # 🔒 SECURITY: Admin operation, moderate limit
async def add_book(
    http_request: Request,
    request: CreateBookRequest,
    facade: Annotated[FacadeBook, Depends(get_book_facade)]
):
    """
    Create a new book (admin only).
    
    🔒 SECURITY: Rate limited to prevent excessive book creation.
    """
    command = BookAPIMapper.to_create_command(request)
    book_result = await facade.create_book(command)
    return BookAPIMapper.from_entity_to_create_response(book_result)



@router.get(
    "/",
    response_model=List[GetBooksResponse],
    status_code=status.HTTP_200_OK,
)
@limiter.limit("60/minute")  # 🔒 SECURITY: List operations
async def get_all_books(
    request: Request,
    facade: Annotated[FacadeBook, Depends(get_book_facade)]
):
    """
    Get all books.
    
    🔒 SECURITY: Rate limited as list operations are database-intensive.
    """
    enriched_books = await facade.get_all_books()
    return [
        BookAPIMapper.from_enriched_dict_to_response(book)
        for book in enriched_books
    ]
    



@router.get(
    "/{book_id}", 
    response_model=BookFullResponseDTO,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("100/minute")  # 🔒 SECURITY: High-frequency read operation
async def get_book_details(
    request: Request,
    book_id: str,
    facade: Annotated[FacadeBook, Depends(get_book_facade)]
):
    """
    Get book details by ID.
    
    🔒 SECURITY: Higher limit for read operations.
    """
    response_dto = await facade.get_book_by_id(book_id) 
    return BookAPIMapper.from_full_details_to_response(response_dto)
   
    
    
@router.put(
    "/{book_id}", 
    response_model=GetBooksResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_role_checker)]
)
@limiter.limit("30/minute")  # 🔒 SECURITY: Update operations
async def update_book(
    request: Request,
    book_id: str,
    update_request: UpdateBookDTO,
    facade: Annotated[FacadeBook, Depends(get_book_facade)]
):
    """
    Update a book (admin only).
    
    🔒 SECURITY: Rate limited to prevent excessive updates.
    """
    command = BookAPIMapper.to_update_command(update_request)
    book_result = await facade.update_book(book_id, command)
    return BookAPIMapper.from_update_result_to_response(book_result)
    


@router.delete(
    "/{book_id}", 
    response_model=BookMessage,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_role_checker)]
)
@limiter.limit("20/minute")  # 🔒 SECURITY: Destructive operation
async def delete_book(
    request: Request,
    book_id: str,
    facade: Annotated[FacadeBook, Depends(get_book_facade)]
):
    """
    Delete a book (admin only).
    
    🔒 SECURITY: Rate limited as this is a destructive operation.
    """
    await facade.delete_book(book_id)
    return BookMessage(
        message=f"Book Deleted"
    )
