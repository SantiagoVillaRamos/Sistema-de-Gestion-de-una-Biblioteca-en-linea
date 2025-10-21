from fastapi import APIRouter, Depends, status
from typing import Annotated
from application.facade.facade_auth import AuthFacade
from infrastructure.web.dependencie import get_auth_facade, RoleChecker
from infrastructure.web.models import LoginRequest, LoginResponse
from application.dto.user_command_dto import LoginUserCommand

admin_role_checker = RoleChecker(["ADMIN"])

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
    
)
async def login_for_access_token(
    request: LoginRequest,
    facade: Annotated[AuthFacade, Depends(get_auth_facade)]
):
    command = LoginUserCommand(
        email=request.email,
        password=request.password
    )
    response_dto = await facade.login_user_facade(command)
    return LoginResponse(token=response_dto.token)
