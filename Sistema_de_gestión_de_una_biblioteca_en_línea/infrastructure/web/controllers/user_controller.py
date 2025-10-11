from fastapi import APIRouter, Depends, status
from application.facade.facade_user import UserFacade
from infrastructure.web.dependencies import get_user_facade
from infrastructure.web.models import UserCreationResponse, GetUserResponse, CreateUserRequest
from application.dto.user_command_dto import CreateUserCommand, GetUserCommand
from typing import Annotated


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreationResponse
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
        user_type=request.user_type
    )
    return await facade.create_user_facade(command)

    
    
@router.get(
    "/{user_id}", 
    status_code=status.HTTP_200_OK,
    response_model=GetUserResponse
)
async def get_user(
    user_id: str,
    facade: Annotated[UserFacade, Depends(get_user_facade)]
):
    # 2. Construir el DTO (Command) que la fachada espera
    command = GetUserCommand(user_id=user_id)
    return await facade.get_user_facade(command)
    
        
