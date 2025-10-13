from application.use_cases.user.login_user_use_case import LoginUserUseCase
from application.dto.user_command_dto import LoginUserCommand, LoginUserResponse

class AuthFacade:
    
    def __init__(self, login_user_use_case: LoginUserUseCase):
        self._login_user_use_case = login_user_use_case

    async def login_user_facade(self, command: LoginUserCommand) -> LoginUserResponse:
        return await self._login_user_use_case.execute(command)
