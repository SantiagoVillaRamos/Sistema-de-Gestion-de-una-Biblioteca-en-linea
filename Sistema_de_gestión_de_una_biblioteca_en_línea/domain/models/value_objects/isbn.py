from __future__ import annotations
from dataclasses import dataclass
from domain.models.exceptions.business_exception import BusinessNotFoundError

@dataclass(frozen=True)
class ISBN:
   
    value: str

    def __post_init__(self):
        # Eliminar guiones y espacios
        processed_isbn = self.value.replace('-', '').replace(' ', '')

        if not (len(processed_isbn) == 10 or len(processed_isbn) == 13) or not processed_isbn.isdigit():
            raise BusinessNotFoundError(self.value, "El ISBN debe tener 10 o 13 dígitos.")
        

    def __eq__(self, other) -> bool:
        """
        Define la igualdad para los Objetos de Valor.
        Dos ISBN son iguales si sus valores son idénticos.
        """
        if not isinstance(other, ISBN):
            return NotImplemented
        return self.value == other.value

    def __hash__(self):
        """
        Hace que el objeto sea hasheable, necesario para sets y diccionarios.
        """
        return hash(self.value)