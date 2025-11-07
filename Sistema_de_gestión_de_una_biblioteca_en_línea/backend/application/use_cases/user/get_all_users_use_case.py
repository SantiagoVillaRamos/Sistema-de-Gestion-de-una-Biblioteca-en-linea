from typing import List
from domain.models.user import User
from domain.ports.user_repository import UserRepository
from application.ports.user.get_all_users import GetAllUsers

class GetAllUsersUseCase(GetAllUsers):
    
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    async def get_all(self) -> List[User]:
       
        return await self.user_repo.find_all()
    
    