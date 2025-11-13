from domain.ports.user_repository import UserRepository
from domain.models.factory.userFactory import UserFactory
from domain.models.user import User
from application.dto.user_command_dto import CreateUserCommand
from application.ports.user.user_creater import UserCreate
from domain.models.exceptions.business_exception import BusinessConflictError

class CreateUserUseCase(UserCreate):

    def __init__(self, user_repository: UserRepository, user_factory: UserFactory):
        self.user_repo = user_repository
        self.user_factory = user_factory

    async def create(self, command: CreateUserCommand) -> User:
        
        existing_user = await self.user_repo.find_by_email((command.email))
        if existing_user:
            raise BusinessConflictError(command.email, "El usuario con este email ya existe")
        
        new_user = self.user_factory.create_user_factory(
            name=command.name,
            email=command.email,
            password=command.password,
            roles=command.roles,
            user_type=command.user_type
        )
        
        await self.user_repo.save(new_user)
        
        return new_user
    
