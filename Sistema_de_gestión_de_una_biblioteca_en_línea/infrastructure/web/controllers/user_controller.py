from fastapi import APIRouter, Depends, status
from application.facade.facade_user import UserFacade
from infrastructure.web.dependencie import get_user_facade
from infrastructure.web.model.user_models import UserCreationResponse, GetUserResponse, CreateUserRequest
from infrastructure.web.mappers.user_api_mapper import UserAPIMapper
from infrastructure.web.dependencies.auth_validators import validate_admin_creation, validate_user_access
from typing import Annotated



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreationResponse,
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
    # auth_check: Annotated[None, Depends(validate_user_access)],
    facade: Annotated[UserFacade, Depends(get_user_facade)],
    
):
        
    details_dto = await facade.get_user_facade(user_id)
    return UserAPIMapper.from_details_dto_to_get_response(details_dto)

