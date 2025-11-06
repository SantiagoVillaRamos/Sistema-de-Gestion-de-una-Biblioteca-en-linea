from dataclasses import dataclass
from domain.models.exceptions.business_exception import BusinessConflictError

@dataclass(frozen=True)
class Email:
   
    address: str

    def __post_init__(self):
        
        if not self._is_valid_email(self.address):
            raise BusinessConflictError(self.address, "Dirección de correo electrónico inválida.")
        # Guardar el valor limpio
        if isinstance(self.address, str):
            object.__setattr__(self, 'address', self.address.strip())
        else:
            # Si pasó la validación de _is_valid_email (lo cual solo debería pasar si es str),
            # este caso es solo un safety net.
            object.__setattr__(self, 'address', self.address)
            
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Valida el formato del correo electrónico."""
        if email is None or not isinstance(email, str):
            return False
        
        cleaned_email = email.strip()
        
        if not cleaned_email or not cleaned_email.strip():
            return False
                
        # Validación de dominios específicos
        if not cleaned_email.endswith(("@gmail.com", "@yahoo.com", "@outlook.com")):
            return False
            
        # Validación básica de estructura (debe contener '@' y '...')
        # Se elimina la validación del punto, confiando en el endswith para dominios
        if '@' not in cleaned_email:
            return False
            
        return True
    

    
    