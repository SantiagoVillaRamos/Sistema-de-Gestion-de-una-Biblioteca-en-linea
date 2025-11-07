from abc import ABC, abstractmethod
from application.dto.user_command_dto import LoginUserCommand, LoginUserResponseToken

class Auth(ABC):
    
    @abstractmethod
    async def auth(self, command: LoginUserCommand) -> LoginUserResponseToken:
        pass
