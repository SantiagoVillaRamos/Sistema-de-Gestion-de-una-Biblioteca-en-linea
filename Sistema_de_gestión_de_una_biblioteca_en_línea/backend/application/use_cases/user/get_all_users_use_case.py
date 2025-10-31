from typing import List
from domain.models.user import User
from application.ports.user_repository import UserRepository

class GetAllUsersUseCase:
    
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository

    async def execute(self) -> List[User]:
       
        return await self.user_repo.find_all()
    
    