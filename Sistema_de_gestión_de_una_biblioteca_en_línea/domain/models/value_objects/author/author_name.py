from dataclasses import dataclass
from domain.models.exceptions.business_exception import BusinessTypeError 

@dataclass(frozen=True)
class AuthorName:
    
    value: str

    def __post_init__(self):

        if not self.value or not self.value.strip():
            raise BusinessTypeError("El nombre del autor no puede estar vacío.")
       
        if len(self.value) > 100:
            raise BusinessTypeError("El nombre del autor no puede exceder los 100 caracteres.")
            
        # Estandarizar el valor (ej. limpiar espacios, capitalizar)
        object.__setattr__(self, 'value', self.value.strip().title())