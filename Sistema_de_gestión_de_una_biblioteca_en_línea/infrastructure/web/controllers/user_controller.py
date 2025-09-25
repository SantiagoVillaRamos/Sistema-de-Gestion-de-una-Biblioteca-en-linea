from fastapi import APIRouter, Depends, status
from application.facade.facade_user import UserFacade
from infrastructure.web.dependencies import get_user_facade
from infrastructure.web.models import UserCreationResponse, GetUserResponse, CreateUserCommand
from typing import Annotated


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/users", 
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreationResponse
)
async def create_user(
    command: CreateUserCommand,
    facade: Annotated[UserFacade, Depends(get_user_facade)]
):
    return await facade.create_user_facade(command)
    
    
    
@router.get(
    "/users/{user_id}", 
    status_code=status.HTTP_200_OK,
    response_model=GetUserResponse
)
async def get_user(
    user_id: str,
    facade: Annotated[UserFacade, Depends(get_user_facade)]
):
    return await facade.get_user_facade(user_id)
    
        
