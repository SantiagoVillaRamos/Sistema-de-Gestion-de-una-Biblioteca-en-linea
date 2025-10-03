from dataclasses import dataclass
from domain.models.exceptions.business_exception import BusinessNotFoundError
import re

@dataclass(frozen=True)
class Password:
    
    hashed: str

    def __post_init__(self):
        if not self._is_valid_password(self.hashed):
            raise BusinessNotFoundError(self.hashed, "La contraseña no cumple con los requisitos de seguridad.")

    @staticmethod
    def _is_valid_password(password: str) -> bool:
        
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        return True