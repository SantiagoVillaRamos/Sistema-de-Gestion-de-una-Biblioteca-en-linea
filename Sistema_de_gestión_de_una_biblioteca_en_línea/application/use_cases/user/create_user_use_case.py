from application.ports.user_repository import UserRepository
from domain.models.user import User
from application.dto.user_command_dto import CreateUserCommand, CreateUserResponse
from domain.models.factory.userFactory import UserFactory

class CreateUserUseCase:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, command: CreateUserCommand) -> str:
        
        new_user = UserFactory.create(
            name=command.name,
            email=command.email,
            password=command.password
        )
        
        await self.user_repo.save(new_user)
        
        return self._build_user_response(new_user)
    
    
    def _build_user_response(self, new_user: User) -> CreateUserResponse:
        return CreateUserResponse(
            user_id=new_user.user_id,
            name=new_user.name,
            email=new_user.email.address,
            password=new_user.password.hashed
        )
        
    
