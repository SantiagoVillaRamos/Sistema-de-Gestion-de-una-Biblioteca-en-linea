
from application.dto.user_command_dto import CreateUserCommand, GetUserCommand, CreateUserResponse, GetUserResponse, UserListResponseItem, UpdateUserCommand

from application.ports.user.user_updater import UserUpdater
from application.ports.user.user_creater import UserCreate
from application.ports.user.delete_user import DeleteUser
from application.ports.user.get_all_users import GetAllUsers
from application.ports.user.get_user_loaner import GetUserLoaner
from application.ports.user.get_user import GetUser

from domain.models.user import User
from typing import Optional


class UserFacade:
    
    def __init__(
        self, 
        create_user_use_case: UserCreate, 
        get_user_use_case: GetUser,
        get_all_users_use_case: GetAllUsers,
        update_current_user_uc: UserUpdater,
        get_user_loan_history_use_case: GetUserLoaner,
        delete_user_use_case: DeleteUser
    ):
        self._create_user_use_case = create_user_use_case
        self._get_user_use_case = get_user_use_case
        self._get_all_users_use_case = get_all_users_use_case
        self._update_current_user_uc = update_current_user_uc
        self._get_user_loan_history_use_case = get_user_loan_history_use_case
        self._delete_user_use_case = delete_user_use_case

    async def create_user_facade(self, command: CreateUserCommand) -> CreateUserResponse:
        return await self._create_user_use_case.create(command)
    
    
    async def get_user_facade(self, command: GetUserCommand) -> Optional[GetUserResponse]:
        return await self._get_user_use_case.get_user(command)
    
    async def get_all_users(self) -> list[UserListResponseItem]:
        return await self._get_all_users_use_case.get_all()
    
    async def update_current_user(self, command: UpdateUserCommand) -> User:
        return await self._update_current_user_uc.update(command)
    
    async def get_user_loan_history(self, user_id: str):
        return await self._get_user_loan_history_use_case.get_user_loan(user_id)
    
    async def delete_user(self, user_id: str) -> None:
        return await self._delete_user_use_case.delete(user_id)