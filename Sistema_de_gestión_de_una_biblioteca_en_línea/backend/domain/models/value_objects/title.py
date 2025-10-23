from dataclasses import dataclass
from domain.models.exceptions.business_exception import BusinessNotFoundError

@dataclass(frozen=True)
class Title:
    
    value: str

    def __post_init__(self):
        
        if not self.value or not self.value.strip():
            raise BusinessNotFoundError(self.value, "El título no puede estar vacío.")

    def __eq__(self, other) -> bool:
        """
        Define la igualdad para los Objetos de Valor.
        Dos títulos son iguales si sus valores son idénticos.
        """
        if not isinstance(other, Title):
            return NotImplemented
        return self.value == other.value

    def __hash__(self):
        """
        Hace que el objeto sea hasheable, necesario para sets y diccionarios.
        """
        return hash(self.value)