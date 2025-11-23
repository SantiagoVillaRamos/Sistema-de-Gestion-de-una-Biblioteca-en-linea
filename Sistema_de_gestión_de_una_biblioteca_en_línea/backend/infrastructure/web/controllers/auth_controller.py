from fastapi import APIRouter, Depends, status, Request, HTTPException
from typing import Annotated
from application.facade.facade_auth import AuthFacade
from infrastructure.web.dependencie import get_auth_facade, get_current_user, repos
from infrastructure.web.models import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    LogoutRequest,
    MessageResponse
)
from infrastructure.web.mappers.login_mapper import LoginMapper
from slowapi import Limiter
from slowapi.util import get_remote_address
from domain.models.user import User
from datetime import datetime, timedelta, timezone

# 🔒 SECURITY: Initialize rate limiter for this router
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
    tags=["Authentication"]
)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse
)
@limiter.limit("5/minute")  # 🔒 SECURITY: Max 5 login attempts per minute
async def login_for_access_token(
    request: Request,
    login_request: LoginRequest,
    facade: Annotated[AuthFacade, Depends(get_auth_facade)]
):
    """
    Authenticate user and return JWT tokens.
    
    🔒 SECURITY: 
    - Rate limited to prevent brute force attacks
    - Returns both access and refresh tokens
    - Access token expires in 15 minutes
    - Refresh token expires in 7 days
    """
    command = LoginMapper.to_login_command(login_request)
    response_dto = await facade.login_user_facade(command)
    
    # Get user to fetch roles for token pair
    user = await repos.user_repo.find_by_email(login_request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create token pair (access + refresh)
    token_pair = repos.auth_service.create_token_pair(user.user_id, user.roles)
    
    return LoginResponse(
        access_token=token_pair["access_token"],
        refresh_token=token_pair["refresh_token"],
        token_type=token_pair["token_type"]
    )


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    response_model=RefreshTokenResponse
)
@limiter.limit("10/minute")  # 🔒 SECURITY: Rate limit refresh endpoint
async def refresh_access_token(
    request: Request,
    refresh_request: RefreshTokenRequest
):
    """
    Refresh access token using a valid refresh token.
    
    🔒 SECURITY:
    - Validates refresh token
    - Checks if token is blacklisted
    - Fetches fresh user data from database
    - Returns new access token
    """
    # Check if refresh token is blacklisted
    if repos.token_blacklist.is_blacklisted(refresh_request.refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked"
        )
    
    # Validate refresh token and get user_id
    try:
        user_id = repos.auth_service.validate_refresh_token(refresh_request.refresh_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Fetch fresh user data
    user = await repos.user_repo.find_by_id(user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new access token with fresh roles
    new_access_token = repos.auth_service.create_access_token(user.user_id, user.roles)
    
    return RefreshTokenResponse(
        access_token=new_access_token,
        token_type="bearer"
    )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_model=MessageResponse
)
async def logout(
    logout_request: LogoutRequest,
    current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Logout user by blacklisting their tokens.
    
    🔒 SECURITY:
    - Requires authentication
    - Blacklists both access and refresh tokens
    - Prevents token reuse after logout
    """
    # Calculate token expiration times
    access_token_expiry = datetime.now(timezone.utc) + timedelta(minutes=15)
    refresh_token_expiry = datetime.now(timezone.utc) + timedelta(days=7)
    
    # Add tokens to blacklist
    repos.token_blacklist.add_token(logout_request.access_token, access_token_expiry)
    repos.token_blacklist.add_token(logout_request.refresh_token, refresh_token_expiry)
    
    return MessageResponse(message="Successfully logged out")
