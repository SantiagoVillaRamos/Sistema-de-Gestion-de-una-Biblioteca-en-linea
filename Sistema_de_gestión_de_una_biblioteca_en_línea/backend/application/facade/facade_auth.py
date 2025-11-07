
from application.dto.user_command_dto import LoginUserCommand, LoginUserResponseToken
from application.ports.auth.auth_user import Auth

class AuthFacade:
    
    def __init__(self, login_user_use_case: Auth):
        self._login_user_use_case = login_user_use_case

    async def login_user_facade(self, command: LoginUserCommand) -> LoginUserResponseToken:
        return await self._login_user_use_case.auth(command)
