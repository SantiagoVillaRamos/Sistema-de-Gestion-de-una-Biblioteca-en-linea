
from application.dto.user_command_dto import LoginUserCommand, LoginUserResponseToken
from infrastructure.web.models import LoginRequest, LoginResponse


class LoginMapper:    
    @staticmethod
    def to_login_command(request: LoginRequest) -> LoginUserCommand:
        """Mapea el DTO de entrada HTTP al Comando de Login."""
        return LoginUserCommand(
            email=request.email,
            password=request.password
        )
        
    @staticmethod
    def from_login_response(response: LoginUserResponseToken) -> LoginResponse:
        """Mapea el DTO de respuesta del caso de uso al DTO de respuesta HTTP."""
        return LoginResponse(
            token=response.token
        )
