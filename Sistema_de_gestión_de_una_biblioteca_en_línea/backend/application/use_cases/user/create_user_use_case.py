from application.ports.user_repository import UserRepository
from domain.models.factory.userFactory import UserFactory
from domain.models.user import User
from application.dto.user_command_dto import CreateUserCommand


class CreateUserUseCase:

    def __init__(self, user_repository: UserRepository, user_factory: UserFactory):
        self.user_repo = user_repository
        self.user_factory = user_factory

    async def execute(self, command: CreateUserCommand) -> User:
        
        new_user = self.user_factory.create(
            name=command.name,
            email=command.email,
            password=command.password,
            roles=command.roles,
            user_type=command.user_type
        )
        
        await self.user_repo.save(new_user)
        
        return new_user
    
