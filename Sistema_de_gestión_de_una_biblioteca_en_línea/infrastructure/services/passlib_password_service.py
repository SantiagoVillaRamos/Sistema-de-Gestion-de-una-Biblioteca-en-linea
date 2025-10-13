from passlib.context import CryptContext
from domain.ports.PasswordService import PasswordService

class PasslibPasswordService(PasswordService):

    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, plain_password: str) -> str:
        return self.context.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.context.verify(plain_password, hashed_password)
