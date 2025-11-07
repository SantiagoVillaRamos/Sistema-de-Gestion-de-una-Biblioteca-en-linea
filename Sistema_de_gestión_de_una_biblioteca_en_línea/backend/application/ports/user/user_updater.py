from abc import ABC, abstractmethod
from domain.models.user import User
from application.dto.user_command_dto import UpdateUserCommand


class UserUpdater(ABC):
    
    @abstractmethod
    async def update(self, command: UpdateUserCommand) -> User:
        pass

