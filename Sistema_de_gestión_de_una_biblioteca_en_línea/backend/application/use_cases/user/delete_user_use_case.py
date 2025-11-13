
from domain.ports.user_repository import UserRepository 
from application.ports.user.delete_user import DeleteUser
from domain.models.exceptions.business_exception import BusinessNotFoundError

class DeleteUserUseCase(DeleteUser):
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def delete(self, user_id: str) -> None:
        
        persistence_data = await self.user_repo.find_by_id(user_id)
        if not persistence_data:
            raise BusinessNotFoundError(user_id, "Usuario no encontrado")
        
        await self.user_repo.delete(persistence_data)
        
        