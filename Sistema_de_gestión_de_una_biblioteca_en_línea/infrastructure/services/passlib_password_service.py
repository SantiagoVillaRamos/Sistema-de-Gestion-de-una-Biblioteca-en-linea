from passlib.context import CryptContext
from domain.ports.PasswordService import PasswordService
from domain.models.exceptions.business_exception import BusinessUnauthorizedError

class PasslibPasswordService(PasswordService):

    def __init__(self):
        self.context = CryptContext(schemes=["argon2"], deprecated="auto")

    def hash_password(self, plain_password: str) -> str:
        
        if isinstance(plain_password, bytes):
            plain_password = plain_password.decode('utf-8')
        return self.context.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        
        password_is_valid = self.context.verify(plain_password, hashed_password)
        if not password_is_valid:
            raise BusinessUnauthorizedError("Contraseña incorrecta.")
        return password_is_valid 
