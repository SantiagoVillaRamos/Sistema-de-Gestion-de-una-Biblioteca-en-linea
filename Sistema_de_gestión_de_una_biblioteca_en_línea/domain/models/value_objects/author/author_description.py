from dataclasses import dataclass
from domain.models.exceptions.business_exception import BusinessTypeError 


@dataclass(frozen=True)
class AuthorDescription:
    
    value: str

    def __post_init__(self):
        # Normalizar: Si es None o solo espacios, se convierte a string vacío para consistencia.
        if self.value is None:
            object.__setattr__(self, 'value', '')
            return
            
        cleaned_value = self.value.strip()
        
        # 1. Validación de longitud máxima
        if len(cleaned_value) > 500:
            raise BusinessTypeError("La descripción del autor no puede exceder los 500 caracteres.")
            
        # Guardar el valor limpio
        object.__setattr__(self, 'value', cleaned_value)