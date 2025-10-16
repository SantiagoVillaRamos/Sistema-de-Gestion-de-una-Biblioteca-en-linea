from application.ports.user_repository import UserRepository
from domain.models.user import User
from application.dto.user_command_dto import CreateUserCommand, CreateUserResponse
from domain.models.factory.userFactory import UserFactory

class CreateUserUseCase:

    def __init__(self, user_repository: UserRepository, user_factory: UserFactory):
        self.user_repo = user_repository
        self.user_factory = user_factory

    async def execute(self, command: CreateUserCommand) -> CreateUserResponse:
        # El caso de uso extrae los datos del DTO y los pasa a la factoría de dominio.
        new_user = self.user_factory.create(
            name=command.name,
            email=command.email,
            password=command.password,
            roles=command.roles,
            user_type=command.user_type
        )
        
        await self.user_repo.save(new_user)
        
        return self._build_user_response(new_user)
    
    def _build_user_response(self, new_user: User) -> CreateUserResponse:
        return CreateUserResponse(
            user_id=new_user.user_id,
            name=new_user.name,
            email=new_user.email.address,
            user_type=new_user.user_type,
            roles=new_user.roles
        )
