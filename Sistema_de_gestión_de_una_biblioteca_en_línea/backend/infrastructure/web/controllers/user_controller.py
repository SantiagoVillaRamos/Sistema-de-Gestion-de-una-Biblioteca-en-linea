from fastapi import APIRouter, Depends, status, Response, Request
from application.facade.facade_user import UserFacade
from infrastructure.web.dependencie import get_user_facade
from infrastructure.web.model.user_models import UserResponse, GetUserResponse, CreateUserRequest, UserListResponse, UpdateUserRequest, UserLoanHistoryResponse
from infrastructure.web.mappers.user_api_mapper import UserAPIMapper
from infrastructure.web.dependencies.auth_validators import validate_admin_creation, validate_user_access, validate_admin_only, get_current_user, validate_admin_delete
from typing import Annotated
from domain.models.user import User
from slowapi import Limiter
from slowapi.util import get_remote_address


# 🔒 SECURITY: Initialize rate limiter for this router
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    tags=["Users"]
)


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
@limiter.limit("10/minute")  # 🔒 SECURITY: Prevent spam registration
async def create_user(
    request: Request,
    user_request: CreateUserRequest,
    #auth_check: Annotated[None, Depends(validate_admin_creation)],
    facade: Annotated[UserFacade, Depends(get_user_facade)]
):
    """
    Create a new user.
    
    🔒 SECURITY: Rate limited to prevent spam registration.
    """
    command = UserAPIMapper.to_create_command(user_request)
    object_user = await facade.create_user_facade(command)
    return UserAPIMapper.from_entity_to_creation_response(object_user)

    
    
@router.get(
    "/{user_id}", 
    status_code=status.HTTP_200_OK, 
    response_model=GetUserResponse
)
@limiter.limit("60/minute")  # 🔒 SECURITY: Read operations can be more frequent
async def get_user(
    request: Request,
    user_id: str,
    auth_check: Annotated[None, Depends(validate_user_access)],
    facade: Annotated[UserFacade, Depends(get_user_facade)],
    
):    
    """
    Get user details by ID.
    
    🔒 SECURITY: Rate limited for read operations.
    """
    details_dto = await facade.get_user_facade(user_id)
    return UserAPIMapper.from_details_dto_to_get_response(details_dto)


@router.get(
    "/", 
    status_code=status.HTTP_200_OK, 
    response_model=UserListResponse
)
@limiter.limit("30/minute")  # 🔒 SECURITY: List operations are expensive
async def list_users(
    request: Request,
    auth_check: Annotated[None, Depends(validate_admin_only)], 
    facade: Annotated[UserFacade, Depends(get_user_facade)],
):
    """
    List all users (admin only).
    
    🔒 SECURITY: Rate limited as list operations are database-intensive.
    """
    users = await facade.get_all_users()
    return UserAPIMapper.from_entity_list_to_response(users)



@router.put(
    "/me", 
    status_code=status.HTTP_200_OK, 
    response_model=UserResponse 
)
@limiter.limit("20/minute")  # 🔒 SECURITY: Reasonable update frequency
async def update_user_me(
    request: Request,
    update_request: UpdateUserRequest,
    facade: Annotated[UserFacade, Depends(get_user_facade)],
    current_user: Annotated[User, Depends(get_current_user)], 
):
    """
    Update current user's profile.
    
    🔒 SECURITY: Rate limited to prevent excessive updates.
    """
    command = UserAPIMapper.to_update_command(
        request=update_request, 
        user_id=current_user.user_id 
    )
    updated_user = await facade.update_current_user(command)
    return UserAPIMapper.from_entity_to_update_response(updated_user)



@router.get(
    "/me/loans", 
    status_code=status.HTTP_200_OK, 
    response_model=UserLoanHistoryResponse
)
@limiter.limit("60/minute")  # 🔒 SECURITY: Read operations
async def get_my_loan_history(
    request: Request,
    facade: Annotated[UserFacade, Depends(get_user_facade)],
    current_user: Annotated[User, Depends(get_current_user)], 
):
    """
    Get current user's loan history.
    
    🔒 SECURITY: Rate limited for read operations.
    """
    history_dto = await facade.get_user_loan_history(current_user.user_id)
    return UserAPIMapper.from_loan_history_dto_to_response(history_dto)



@router.delete(
    "/{user_id}", 
    status_code=status.HTTP_204_NO_CONTENT
)
@limiter.limit("10/minute")  # 🔒 SECURITY: Destructive operation
async def delete_user(
    request: Request,
    user_id: str,
    auth_check: Annotated[None, Depends(validate_admin_delete)], 
    facade: Annotated[UserFacade, Depends(get_user_facade)],
):
    """
    Delete a user (admin only).
    
    🔒 SECURITY: Rate limited as this is a destructive operation.
    """
    await facade.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

