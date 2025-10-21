from application.use_cases.user.create_user_use_case import CreateUserUseCase
from application.dto.user_command_dto import CreateUserCommand, GetUserCommand, CreateUserResponse, GetUserResponse, UserListResponseItem
from application.use_cases.user.get_user_use_case import GetUserUseCase
from application.use_cases.user.get_all_users_use_case import GetAllUsersUseCase

from typing import Optional


class UserFacade:
    
    def __init__(
        self, 
        create_user_use_case: CreateUserUseCase, 
        get_user_use_case: GetUserUseCase,
        get_all_users_use_case: GetAllUsersUseCase
    ):
        self._create_user_use_case = create_user_use_case
        self._get_user_use_case = get_user_use_case
        self._get_all_users_use_case = get_all_users_use_case

    async def create_user_facade(self, command: CreateUserCommand) -> CreateUserResponse:
        return await self._create_user_use_case.execute(command)
    
    
    async def get_user_facade(self, command: GetUserCommand) -> Optional[GetUserResponse]:
        return await self._get_user_use_case.execute(command)
    
    async def get_all_users(self) -> list[UserListResponseItem]:
        return await self._get_all_users_use_case.execute()