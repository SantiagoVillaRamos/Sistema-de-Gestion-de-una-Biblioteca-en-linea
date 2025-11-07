
from domain.ports.user_repository import UserRepository 
from application.ports.user.delete_user import DeleteUser

class DeleteUserUseCase(DeleteUser):
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def delete(self, user_id: str) -> None:
        
        user = await self.user_repo.find_by_id(user_id)
        await self.user_repo.delete(user)
        
        