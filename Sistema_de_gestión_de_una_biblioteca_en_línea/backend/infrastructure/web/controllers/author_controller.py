from fastapi import APIRouter, Depends, status, Request
from typing import Annotated, List
from application.facade.facade_author import AuthorFacade
from infrastructure.web.dependencie import get_author_facade, RoleChecker
from infrastructure.web.model.author_dtos import CreateAuthorRequest, CreateAuthorResponse, AuthorDetailResponse, UpdateAuthorRequest, AuthorMessage
from infrastructure.web.mappers.author_api_mapper import AuthorAPIMapper
from slowapi import Limiter
from slowapi.util import get_remote_address

admin_role_checker = RoleChecker(["ADMIN"])

# 🔒 SECURITY: Initialize rate limiter for this router
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    tags=["Authors"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateAuthorResponse,
    dependencies=[Depends(admin_role_checker)]
)
@limiter.limit("30/minute")  # 🔒 SECURITY: Admin operation
async def add_author(
    http_request: Request,
    request: CreateAuthorRequest,
    facade: Annotated[AuthorFacade, Depends(get_author_facade)]
):
    """
    Create a new author (admin only).
    
    🔒 SECURITY: Rate limited to prevent excessive author creation.
    """
    command = AuthorAPIMapper.to_create_command(request)
    new_author = await facade.create_author_facade(command)
    return AuthorAPIMapper.from_entity_to_create_response(new_author)



@router.get(
    "/", 
    response_model=List[CreateAuthorResponse],
    status_code=status.HTTP_200_OK,
)
@limiter.limit("60/minute")  # 🔒 SECURITY: List operations
async def get_all_authors(
    request: Request,
    facade: Annotated[AuthorFacade, Depends(get_author_facade)]
):
    """
    Get all authors.
    
    🔒 SECURITY: Rate limited as list operations are database-intensive.
    """
    authors = await facade.get_all_authors()
    return AuthorAPIMapper.from_entity_list_to_response_list(authors)



@router.get(
    "/{author_id}", 
    response_model=AuthorDetailResponse,
    status_code=status.HTTP_200_OK,
)
@limiter.limit("100/minute")  # 🔒 SECURITY: High-frequency read operation
async def get_author_details(
    request: Request,
    author_id: str,
    facade: Annotated[AuthorFacade, Depends(get_author_facade)]
):
    """
    Get author details by ID.
    
    🔒 SECURITY: Higher limit for read operations.
    """
    author_result= await facade.get_author_by_id(author_id) 
    return AuthorAPIMapper.from_details_result_to_response(author_result)



@router.put(
    "/{author_id}", 
    response_model=CreateAuthorResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_role_checker)]
)
@limiter.limit("30/minute")  # 🔒 SECURITY: Update operations
async def update_author(
    request: Request,
    author_id: str,
    update_request: UpdateAuthorRequest,
    facade: Annotated[AuthorFacade, Depends(get_author_facade)],
    
):
    """
    Update an author (admin only).
    
    🔒 SECURITY: Rate limited to prevent excessive updates.
    """
    command = AuthorAPIMapper.to_update_command(update_request)
    updated_author = await facade.update_author_data(author_id, command)
    return AuthorAPIMapper.from_entity_to_create_response(updated_author)


@router.delete(
    "/{author_id}",
    response_model=AuthorMessage, 
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_role_checker)]
)
@limiter.limit("20/minute")  # 🔒 SECURITY: Destructive operation
async def delete_author(
    request: Request,
    author_id: str,
    facade: Annotated[AuthorFacade, Depends(get_author_facade)],
    
):
    """
    Delete an author (admin only).
    
    🔒 SECURITY: Rate limited as this is a destructive operation.
    """
    await facade.delete_author_data(author_id)
    
    return AuthorMessage(
        message=f"Autor eliminado, y todos sus datos han sido eliminados."
    )