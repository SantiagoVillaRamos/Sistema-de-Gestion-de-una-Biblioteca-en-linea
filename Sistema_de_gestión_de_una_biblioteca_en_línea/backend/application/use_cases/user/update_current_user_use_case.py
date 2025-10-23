
from domain.models.user import User
from application.dto.user_command_dto import UpdateUserCommand
from application.ports.user_repository import UserRepository 
from domain.services.UpdateCurrentService import UserUpdaterService

class UpdateCurrentUserUseCase:
    
    def __init__(
        self, 
        user_repo: UserRepository,
        user_updater_service: UserUpdaterService,
    ):
        self.user_repo = user_repo
        self.user_updater_service = user_updater_service
        

    async def execute(self, command: UpdateUserCommand) -> User:
        
        user = await self.user_repo.find_by_id(command.user_id)
        
        update_user_data = self.user_updater_service.update_user_data(user, command)
        await self.user_repo.save(update_user_data)
        
        return update_user_data
    
    