from fastapi import APIRouter, Depends, status, HTTPException
from application.facade.facade_user import UserFacade
from infrastructure.web.dependencies import get_user_facade, RoleChecker, get_current_user
from infrastructure.web.models import UserCreationResponse, GetUserResponse, CreateUserRequest
from application.dto.user_command_dto import CreateUserCommand, GetUserCommand
from typing import Annotated
from domain.models.user import User


admin_role_checker = RoleChecker(["ADMIN"])

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreationResponse,
    dependencies=[Depends(admin_role_checker)]
)
async def create_user(
    request: CreateUserRequest,
    facade: Annotated[UserFacade, Depends(get_user_facade)]
):
    # 1. Traducir el modelo de la petición web (Request) al DTO de la aplicación (Command)
    command = CreateUserCommand(
        name=request.name,
        email=request.email,
        password=request.password,
        roles=request.roles
    )
    return await facade.create_user_facade(command)

    
    
@router.get(
    "/{user_id}", 
    status_code=status.HTTP_200_OK,
    response_model=GetUserResponse
)
async def get_user(
    user_id: str,
    facade: Annotated[UserFacade, Depends(get_user_facade)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    # Authorization check
    if "ADMIN" not in current_user.roles and current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
    
    # 2. Construir el DTO (Command) que la fachada espera
    command = GetUserCommand(user_id=user_id)
    return await facade.get_user_facade(command)
    
        
