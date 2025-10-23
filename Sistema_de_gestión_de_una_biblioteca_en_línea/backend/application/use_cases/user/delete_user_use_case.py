
from application.ports.user_repository import UserRepository 


class DeleteUserUseCase:
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, user_id: str) -> None:
        
        user = await self.user_repo.find_by_id(user_id)
        await self.user_repo.delete(user)