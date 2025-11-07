from abc import ABC, abstractmethod
from domain.models.user import User
from application.dto.user_command_dto import CreateUserCommand


class UserCreate(ABC):
    
    @abstractmethod
    async def create(self, command: CreateUserCommand) -> User:
        pass


