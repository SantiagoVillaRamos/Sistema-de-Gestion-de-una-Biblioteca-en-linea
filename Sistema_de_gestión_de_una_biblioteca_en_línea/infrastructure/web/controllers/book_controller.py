from fastapi import APIRouter, Depends, status

from application.facade.facade_library import LibraryFacade
from infrastructure.web.dependencies import get_book_facade
from infrastructure.web.models import CreateBookRequest, CreateBookResponse
from typing import Annotated


router = APIRouter(
    prefix="/Books",
    tags=["Books"]
)


@router.post(
    "/books", 
    status_code=status.HTTP_201_CREATED,
    response_model=CreateBookResponse
)
async def add_book(
    command: CreateBookRequest,
    lend_use_case: Annotated[LibraryFacade, Depends(get_book_facade)]
):
    return await lend_use_case.create_book_facade(command)
    


