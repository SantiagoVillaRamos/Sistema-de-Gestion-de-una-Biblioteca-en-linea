import uuid
import bcrypt
from domain.models.value_objects.email import Email
from domain.models.value_objects.password import Password
from domain.models.user import User

class UserFactory:
    
    @staticmethod
    def create(name: str, email: str, password:str) -> User:
        
        user_id = str(uuid.uuid4())
        email_vo = Email(email)
        
        # Codifica la clave a bytes para que bcrypt pueda trabajar con ella
        password_bytes = password.encode('utf-8')
        # Genera el hash de la clave (proceso de encriptacion)
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        # Convierte el hash de bytes a string para almacenarlo en la entidad
        hashed_password_str = hashed_password.decode('utf-8')
        password_vo = Password(hashed_password_str)
        
        return User(
            user_id=user_id,
            name=name,
            email=email_vo,
            password=password_vo
        )
        