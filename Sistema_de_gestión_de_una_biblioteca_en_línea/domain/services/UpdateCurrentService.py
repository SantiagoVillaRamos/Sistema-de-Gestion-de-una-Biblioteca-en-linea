from domain.models.user import User
from domain.ports.PasswordService import PasswordService
from domain.models.value_objects.email import Email
from domain.models.value_objects.password import Password
from domain.models.exceptions.business_exception import BusinessError


class UserUpdaterService:
    
    def __init__(self, password_service: PasswordService):
        self.password_service = password_service
        
    def update_user_data(self, user: User, command):
        self._validate_name(command.name)
        
        if self._is_sensitive_change(command):
            self._validate_current_password(user, command.current_password)

        if command.new_email:
            self._update_email(user, command.new_email)
        
        if command.new_password:
            self._update_password(user, command.new_password)
            
        return user
        
    def _validate_name(self, name):
        if name is not None:
            if not name.strip():
                raise BusinessError("El nombre de usuario no puede estar vacío.")
            
    def _is_sensitive_change(self, command):
        return command.new_email or command.new_password
    
    def _validate_current_password(self, user: User, current_password):
        if not current_password:
            raise BusinessError("Se requiere la contraseña actual para cambiar el email o la contraseña.")
        
        if not self.password_service.verify_password(current_password, user.password.hashed):
            raise BusinessError("La contraseña actual es incorrecta.")
            
    def _update_email(self, user: User, new_email):
        new_email_vo = Email(new_email)
        user.email = new_email_vo
        
    def _update_password(self, user: User, new_password):
        hashed_password = self.password_service.hash_password(new_password)
        user.password = Password(hashed_password)
