
from application.ports.user_repository import UserRepository
from application.ports.loan_repository import LoanRepository
from application.ports.book_repository import BookRepository
from application.use_cases.user.create_user_use_case import CreateUserUseCase
from application.dto.user_command_dto import CreateUserCommand, GetUserCommand, CreateUserResponse, GetUserResponse
from application.use_cases.user.get_user_use_case import GetUserUseCase

from typing import Optional


class UserFacade:
    
    def __init__(self, book_repo: BookRepository, user_repo: UserRepository, loan_repo: LoanRepository):
        
        self._create_user_use_case = CreateUserUseCase(user_repo)
        self._get_user_use_case = GetUserUseCase(user_repo, loan_repo, book_repo)

    async def create_user_facade(self, command: CreateUserCommand) -> CreateUserResponse:
        return await self._create_user_use_case.execute(command)
    
    
    async def get_user_facade(self, command: GetUserCommand) -> Optional[GetUserResponse]:
        return await self._get_user_use_case.execute(command)
    
