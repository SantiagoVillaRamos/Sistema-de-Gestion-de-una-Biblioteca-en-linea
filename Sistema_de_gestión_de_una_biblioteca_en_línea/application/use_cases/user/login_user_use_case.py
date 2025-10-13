from application.ports.user_repository import UserRepository
from domain.ports.PasswordService import PasswordService
from application.ports.AuthService import AuthService
from application.dto.user_command_dto import LoginUserCommand, LoginUserResponse
from domain.models.exceptions.business_exception import BusinessUnauthorizedError

class LoginUserUseCase:

    def __init__(self, user_repository: UserRepository, password_service: PasswordService, auth_service: AuthService):
        self.user_repository = user_repository
        self.password_service = password_service
        self.auth_service = auth_service

    async def execute(self, command: LoginUserCommand) -> LoginUserResponse:
        user = await self.user_repository.find_by_email(command.email)
        
        if not user:
            raise BusinessUnauthorizedError("Usuario o contraseña incorrectos.")

        password_is_valid = self.password_service.verify_password(
            plain_password=command.password,
            hashed_password=user.password.hashed
        )

        if not password_is_valid:
            raise BusinessUnauthorizedError("Usuario o contraseña incorrectos.")

        token = self.auth_service.create_token(user_id=user.user_id, roles=user.roles)

        return LoginUserResponse(token=token)
