
from domain.models.user import User
from domain.ports.PasswordService import PasswordService
from domain.models.value_objects.email import Email
from domain.models.value_objects.password import Password

class UserUpdaterService:
    
    def __init__(self, password_service: PasswordService):
        self.password_service = password_service
        
    def update_user_data(self, user: User, command):
        
        if command.name:
            user.name = command.name
            
        if command.new_email:
            new_email_vo = Email(command.new_email)
            user.email = new_email_vo
        
        if command.new_password:
            hashed_password = self.password_service.hash_password(command.new_password)
            user.password = Password(hashed_password)
            
        return user
        