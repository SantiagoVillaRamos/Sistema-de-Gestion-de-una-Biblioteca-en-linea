from domain.ports.user_repository import UserRepository
from domain.ports.PasswordService import PasswordService
from domain.ports.AuthService import AuthService
from application.dto.user_command_dto import LoginUserCommand, LoginUserResponseToken
from domain.models.exceptions.business_exception import BusinessUnauthorizedError
from application.ports.auth.auth_user import Auth

class LoginUserUseCase(Auth):

    def __init__(self, user_repository: UserRepository, password_service: PasswordService, auth_service: AuthService):
        self.user_repository = user_repository
        self.password_service = password_service
        self.auth_service = auth_service

    async def auth(self, command: LoginUserCommand) -> LoginUserResponseToken:
        
        user = await self.user_repository.find_by_email(command.email)
        if not user:
            raise BusinessUnauthorizedError("Usuario o contraseña incorrectos.")

        self.password_service.verify_password(
            plain_password=command.password,
            hashed_password=user.password.hashed
        )

        token = self.auth_service.create_token(user_id=user.user_id, roles=user.roles)

        return LoginUserResponseToken(token=token)
