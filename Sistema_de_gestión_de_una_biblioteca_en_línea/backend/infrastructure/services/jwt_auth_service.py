import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from domain.ports.AuthService import AuthService
from domain.models.exceptions.business_exception import BusinessUnauthorizedError


class JwtAuthService(AuthService):
    """
    JWT Authentication Service with support for access and refresh tokens.
    
    🔒 SECURITY ENHANCEMENTS:
    - Separate access and refresh tokens
    - Shorter access token expiration (15 minutes)
    - Longer refresh token expiration (7 days)
    - Token type identification
    """

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = 15  # 🔒 Reduced from 60 to 15 minutes
        self.refresh_token_expire_days = 7

    def create_token(self, user_id: str, roles: list[str]) -> str:
        """
        Legacy method for backward compatibility.
        Creates an access token.
        """
        return self.create_access_token(user_id, roles)

    def create_access_token(self, user_id: str, roles: list[str]) -> str:
        """
        Create a short-lived access token.
        
        🔒 SECURITY: Expires in 15 minutes for reduced exposure window.
        """
        payload = {
            "sub": user_id,
            "roles": roles,
            "type": "access",  # 🔒 Token type identification
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: str) -> str:
        """
        Create a long-lived refresh token.
        
        🔒 SECURITY: 
        - Expires in 7 days
        - Does not contain roles (must fetch fresh from DB)
        - Used only to obtain new access tokens
        """
        payload = {
            "sub": user_id,
            "type": "refresh",  # 🔒 Token type identification
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(days=self.refresh_token_expire_days)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_token_pair(self, user_id: str, roles: list[str]) -> Dict[str, str]:
        """
        Create both access and refresh tokens.
        
        Returns:
            dict: {
                "access_token": str,
                "refresh_token": str,
                "token_type": "bearer"
            }
        """
        return {
            "access_token": self.create_access_token(user_id, roles),
            "refresh_token": self.create_refresh_token(user_id),
            "token_type": "bearer"
        }

    def validate_token(self, token: str) -> dict[str, Any]:
        """
        Validate and decode a JWT token.
        
        🔒 SECURITY: Validates expiration and signature.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise BusinessUnauthorizedError("Token has expired")
        except jwt.InvalidTokenError:
            raise BusinessUnauthorizedError("Invalid token")

    def validate_refresh_token(self, token: str) -> str:
        """
        Validate a refresh token and return the user_id.
        
        🔒 SECURITY: Ensures token is of type 'refresh'.
        
        Returns:
            str: user_id from token
        
        Raises:
            BusinessUnauthorizedError: If token is invalid or not a refresh token
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # 🔒 Verify it's a refresh token
            if payload.get("type") != "refresh":
                raise BusinessUnauthorizedError("Invalid token type")
            
            user_id = payload.get("sub")
            if not user_id:
                raise BusinessUnauthorizedError("Invalid token payload")
            
            return user_id
            
        except jwt.ExpiredSignatureError:
            raise BusinessUnauthorizedError("Refresh token has expired")
        except jwt.InvalidTokenError:
            raise BusinessUnauthorizedError("Invalid refresh token")
