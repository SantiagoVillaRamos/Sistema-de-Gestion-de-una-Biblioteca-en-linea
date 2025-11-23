
from pydantic import BaseModel, EmailStr, Field


class MessageResponse(BaseModel):
    
    message: str


class LoginRequest(BaseModel):
    """
    Login request model.
    
    🔒 SECURITY: Email validation and password length limit.
    """
    email: EmailStr
    password: str = Field(..., max_length=72, description="User password")


class LoginResponse(BaseModel):
    """
    Login response with access and refresh tokens.
    
    🔒 SECURITY: Returns both tokens for enhanced security.
    """
    access_token: str = Field(..., description="Short-lived access token (15 min)")
    refresh_token: str = Field(..., description="Long-lived refresh token (7 days)")
    token_type: str = Field(default="bearer", description="Token type")


class RefreshTokenRequest(BaseModel):
    """
    Request model for refreshing access token.
    
    🔒 SECURITY: Requires valid refresh token.
    """
    refresh_token: str = Field(..., description="Valid refresh token")


class RefreshTokenResponse(BaseModel):
    """
    Response with new access token.
    
    🔒 SECURITY: Returns new access token without requiring password.
    """
    access_token: str = Field(..., description="New access token")
    token_type: str = Field(default="bearer", description="Token type")


class LogoutRequest(BaseModel):
    """
    Logout request model.
    
    🔒 SECURITY: Blacklists tokens to prevent reuse.
    """
    access_token: str = Field(..., description="Access token to blacklist")
    refresh_token: str = Field(..., description="Refresh token to blacklist")