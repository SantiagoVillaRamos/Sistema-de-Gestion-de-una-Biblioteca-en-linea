
from application.ports.user_repository import UserRepository
from domain.entities.user import User
from application.dto.user_command_dto import CreateUserCommand, CreateUserResponse
from domain.value_objects.email import Email

class CreateUserUseCase:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, command: CreateUserCommand) -> str:
        
        new_user = User(
            name=command.name,
            email=Email(command.email)
        )
        
        await self.user_repo.save(new_user)
        
        return self._build_user_response(new_user)
    
    
    def _build_user_response(self, new_user: User) -> CreateUserResponse:
        return CreateUserResponse(
            user_id=new_user.user_id,
            name=new_user.name,
            email=new_user.email.address
        )
        
    
