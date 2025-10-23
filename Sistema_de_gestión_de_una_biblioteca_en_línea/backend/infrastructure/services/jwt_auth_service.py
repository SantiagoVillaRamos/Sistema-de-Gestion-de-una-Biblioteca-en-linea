import jwt
from datetime import datetime, timedelta, timezone
from typing import Any
from application.ports.AuthService import AuthService
from domain.models.exceptions.business_exception import BusinessUnauthorizedError

class JwtAuthService(AuthService):

    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self, user_id: str, roles: list[str]) -> str:
        payload = {
            "sub": user_id,
            "roles": roles,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)  # Token expires in 1 hour
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def validate_token(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise BusinessUnauthorizedError("El token ha expirado.")
        except jwt.InvalidTokenError:
            raise BusinessUnauthorizedError("Token inválido.")
