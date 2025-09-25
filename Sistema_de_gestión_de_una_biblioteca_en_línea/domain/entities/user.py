from __future__ import annotations
from dataclasses import dataclass, field
from domain.value_objects.email import Email
import uuid

from domain.exceptions.user import UserNotFoundError

@dataclass
class User:
    """Entidad que representa a un usuario en el sistema de biblioteca."""
    user_id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    name: str
    email: Email 
    is_active: bool = True
    
    def __post_init__(self):
        
        if not self.name or not self.name.strip():
            raise UserNotFoundError(self.name, "El nombre no puede estar vacío.")


    def activate(self) -> None:
        """
        Activa la cuenta del usuario.
        """
        self.is_active = True

    def deactivate(self) -> None:
        """
        Desactiva la cuenta del usuario.
        """
        self.is_active = False
        
    