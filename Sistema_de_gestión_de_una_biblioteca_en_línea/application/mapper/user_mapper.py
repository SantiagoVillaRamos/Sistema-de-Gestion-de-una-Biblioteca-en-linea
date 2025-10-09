from domain.models.user import User
from domain.models.value_objects.email import Email
from domain.models.value_objects.password import Password


class UserMapper:
    
    @staticmethod
    def to_entity(data: dict) -> User:
        return User(
            user_id=data.get("user_id"),
            name=data.get("name"),
            email=Email(data.get("email")),
            password=Password(data.get("password"))
        )

    @staticmethod
    def to_dict(user: User) -> dict:
        return {
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email.address,
            "password": user.password.hashed
        }