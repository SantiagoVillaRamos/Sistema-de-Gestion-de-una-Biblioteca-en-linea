from fastapi import APIRouter, Depends, status
from typing import Annotated, List
from application.facade.facade_author import AuthorFacade
from infrastructure.web.dependencies import get_author_facade, RoleChecker
from infrastructure.web.model.author_dtos import CreateAuthorRequest, CreateAuthorResponse, AuthorDetailResponse
from infrastructure.web.mappers.author_api_mapper import AuthorAPIMapper

admin_role_checker = RoleChecker(["ADMIN"])

router = APIRouter(
    prefix="/authors",
    tags=["Authors"]
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateAuthorResponse,
    #dependencies=[Depends(admin_role_checker)]
)
async def add_author(
    request: CreateAuthorRequest,
    facade: Annotated[AuthorFacade, Depends(get_author_facade)]
):
    command = AuthorAPIMapper.to_create_command(request)
    new_author = await facade.create_author_facade(command)
    return AuthorAPIMapper.from_entity_to_create_response(new_author)



@router.get(
    "/", 
    response_model=List[CreateAuthorResponse]
)
async def get_all_authors(
    facade: Annotated[AuthorFacade, Depends(get_author_facade)]
):
    authors = await facade.get_all_authors()
    return AuthorAPIMapper.from_entity_list_to_response_list(authors)



@router.get(
    "/{author_id}", 
    response_model=AuthorDetailResponse
)
async def get_author_details(
    author_id: str,
    facade: Annotated[AuthorFacade, Depends(get_author_facade)]
):
    author, books, author_map = await facade.get_author_by_id(author_id) 
    return AuthorAPIMapper.from_full_details_to_response(author, books, author_map)

