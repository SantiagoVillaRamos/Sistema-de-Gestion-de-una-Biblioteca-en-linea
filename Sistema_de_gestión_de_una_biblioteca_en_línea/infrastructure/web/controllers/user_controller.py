from fastapi import APIRouter, Depends, status
from application.facade.facade_user import UserFacade
from infrastructure.web.dependencie import get_user_facade
from infrastructure.web.model.user_models import UserResponse, GetUserResponse, CreateUserRequest, UserListResponse, UpdateUserRequest
from infrastructure.web.mappers.user_api_mapper import UserAPIMapper
from infrastructure.web.dependencies.auth_validators import validate_admin_creation, validate_user_access, validate_admin_only, get_current_user
from typing import Annotated
from domain.models.user import User



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def create_user(
    request: CreateUserRequest,
    auth_check: Annotated[None, Depends(validate_admin_creation)],
    facade: Annotated[UserFacade, Depends(get_user_facade)],
    
):
    command = UserAPIMapper.to_create_command(request)
    object_user = await facade.create_user_facade(command)
    return UserAPIMapper.from_entity_to_creation_response(object_user)

    
    
@router.get(
    "/{user_id}", 
    status_code=status.HTTP_200_OK, 
    response_model=GetUserResponse
)
async def get_user(
    user_id: str,
    auth_check: Annotated[None, Depends(validate_user_access)],
    facade: Annotated[UserFacade, Depends(get_user_facade)],
    
):
        
    details_dto = await facade.get_user_facade(user_id)
    return UserAPIMapper.from_details_dto_to_get_response(details_dto)


@router.get(
    "/", 
    status_code=status.HTTP_200_OK, 
    response_model=UserListResponse
)
async def list_users(
    
    auth_check: Annotated[None, Depends(validate_admin_only)], 
    facade: Annotated[UserFacade, Depends(get_user_facade)],
):
    
    users = await facade.get_all_users()
    return UserAPIMapper.from_entity_list_to_response(users)




@router.put(
    "/me", 
    status_code=status.HTTP_200_OK, 
    response_model=UserResponse # Reutilizamos el DTO de respuesta
)
async def update_user_me(
    request: UpdateUserRequest,
    facade: Annotated[UserFacade, Depends(get_user_facade)],
    current_user: Annotated[User, Depends(get_current_user)], 
):
    command = UserAPIMapper.to_update_command(
        request=request, 
        user_id=current_user.user_id # <-- Usamos el ID del usuario autenticado
    )
    
    updated_user = await facade.update_current_user(command)
    return UserAPIMapper.from_entity_to_update_response(updated_user)


