from dataclasses import dataclass
from domain.models.exceptions.business_exception import BusinessConflictError

@dataclass(frozen=True)
class Email:
   
    address: str

    def __post_init__(self):
        
        if not self._is_valid_email(self.address):
            raise BusinessConflictError(self.address, "Dirección de correo electrónico inválida:")

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Valida el formato del correo electrónico."""
        if not email.endswith(("@gmail.com", "@yahoo.com", "@outlook.com")):
            return False
        if not email or not email.strip():
            return False
        return True
    

    
    