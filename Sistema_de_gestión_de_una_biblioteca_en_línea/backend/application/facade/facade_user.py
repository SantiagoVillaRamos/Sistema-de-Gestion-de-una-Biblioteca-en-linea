from application.use_cases.user.create_user_use_case import CreateUserUseCase
from application.dto.user_command_dto import CreateUserCommand, GetUserCommand, CreateUserResponse, GetUserResponse, UserListResponseItem, UpdateUserCommand
from application.use_cases.user.get_user_use_case import GetUserUseCase
from application.use_cases.user.update_current_user_use_case import UpdateCurrentUserUseCase
from application.use_cases.user.get_user_loan_history_use_case import GetUserLoanHistoryUseCase
from application.use_cases.user.get_all_users_use_case import GetAllUsersUseCase
from application.use_cases.user.delete_user_use_case import DeleteUserUseCase
from domain.models.user import User
from typing import Optional


class UserFacade:
    
    def __init__(
        self, 
        create_user_use_case: CreateUserUseCase, 
        get_user_use_case: GetUserUseCase,
        get_all_users_use_case: GetAllUsersUseCase,
        update_current_user_uc: UpdateCurrentUserUseCase,
        get_user_loan_history_use_case: GetUserLoanHistoryUseCase,
        delete_user_use_case: DeleteUserUseCase
    ):
        self._create_user_use_case = create_user_use_case
        self._get_user_use_case = get_user_use_case
        self._get_all_users_use_case = get_all_users_use_case
        self._update_current_user_uc = update_current_user_uc
        self._get_user_loan_history_use_case = get_user_loan_history_use_case
        self._delete_user_use_case = delete_user_use_case

    async def create_user_facade(self, command: CreateUserCommand) -> CreateUserResponse:
        return await self._create_user_use_case.execute(command)
    
    
    async def get_user_facade(self, command: GetUserCommand) -> Optional[GetUserResponse]:
        return await self._get_user_use_case.execute(command)
    
    async def get_all_users(self) -> list[UserListResponseItem]:
        return await self._get_all_users_use_case.execute()
    
    async def update_current_user(self, command: UpdateUserCommand) -> User:
        return await self._update_current_user_uc.execute(command)
    
    async def get_user_loan_history(self, user_id: str):
        return await self._get_user_loan_history_use_case.execute(user_id)
    
    async def delete_user(self, user_id: str) -> None:
        return await self._delete_user_use_case.execute(user_id)