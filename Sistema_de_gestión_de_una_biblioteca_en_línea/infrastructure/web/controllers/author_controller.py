from fastapi import APIRouter, Depends, status
from typing import Annotated

from application.facade.facade_author import AuthorFacade
from infrastructure.web.dependencies import get_author_facade, RoleChecker
from infrastructure.web.models import CreateAuthorRequest, CreateAuthorResponse
from application.dto.author_command_dto import CreateAuthorCommand


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
    command = CreateAuthorCommand(name=request.name, description=request.description)
    return await facade.create_author_facade(command)