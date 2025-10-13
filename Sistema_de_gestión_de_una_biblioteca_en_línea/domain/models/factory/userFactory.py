import uuid
from domain.ports.PasswordService import PasswordService
from domain.models.value_objects.email import Email
from domain.models.value_objects.password import Password
from domain.models.user import User

class UserFactory:
    
    def __init__(self, password_service: PasswordService):
        self.password_service = password_service

    def create(self, name: str, email: str, password: str, roles: list[str] = None) -> User:
        
        user_id = str(uuid.uuid4())
        email_vo = Email(email)
        
        hashed_password_str = self.password_service.hash_password(password)
        password_vo = Password(hashed_password_str)
        
        user_roles = roles if roles is not None else ["MEMBER"]
        
        return User(
            user_id=user_id,
            name=name,
            email=email_vo,
            password=password_vo,
            roles=user_roles
        )