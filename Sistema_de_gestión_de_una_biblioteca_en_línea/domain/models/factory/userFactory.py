import uuid
from domain.ports.PasswordService import PasswordService
from domain.models.value_objects.email import Email
from domain.models.value_objects.password import Password
from domain.models.user import User

class UserFactory:
    
    def __init__(self, password_service: PasswordService):
        self.password_service = password_service

    def create(self, name: str, email: str, password: str, roles: list[str] = None, user_type: str = "general") -> User:
        
        user_id = str(uuid.uuid4())
        email_vo = Email(email)
        
        hashed_password_str = self.password_service.hash_password(password)
        password_vo = Password(hashed_password_str)
        
        cleaned_roles = [role for role in roles if role] if roles else []
        user_roles = cleaned_roles if cleaned_roles else ["MEMBER"]
        
        return User(
            user_id=user_id,
            name=name,
            email=email_vo,
            password=password_vo,
            user_type=user_type,
            roles=user_roles
        )