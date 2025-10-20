from fastapi import APIRouter, Depends, status, HTTPException
from application.facade.facade_user import UserFacade
from infrastructure.web.dependencies import get_user_facade, get_optional_current_user
from infrastructure.web.model.user_models import UserCreationResponse, GetUserResponse, CreateUserRequest
from infrastructure.web.mappers.user_api_mapper import UserAPIMapper
from typing import Annotated
from domain.models.user import User


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
    facade: Annotated[UserFacade, Depends(get_user_facade)],
    current_user: Annotated[User | None, Depends(get_optional_current_user)] = None
):
    # Lógica de autorización: solo un admin puede crear otro admin.
    # La creación del PRIMER admin es una excepción a esta regla.
    is_creating_admin = "ADMIN" in (request.roles or [])
    
    if is_creating_admin and current_user and "ADMIN" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can create other administrators."
        )

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
    facade: Annotated[UserFacade, Depends(get_user_facade)],
    # current_user: Annotated[User, Depends(get_optional_current_user)],
):
    
    # if not current_user or (
    #     "ADMIN" not in current_user.roles and current_user.user_id != user_id
    # ):
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="No autorizado para acceder a este recurso",
    #     )
        
    details_dto = await facade.get_user_facade(user_id)
    return UserAPIMapper.from_details_dto_to_get_response(details_dto)
