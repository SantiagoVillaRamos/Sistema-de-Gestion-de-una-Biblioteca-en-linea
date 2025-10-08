from __future__ import annotations
from dataclasses import dataclass, field
from domain.models.value_objects.email import Email
from domain.models.value_objects.password import Password
from domain.models.exceptions.business_exception import BusinessNotFoundError

@dataclass
class User:
    
    user_id: str 
    name: str
    email: Email 
    password: Password
    is_active: bool = True
    
    def __post_init__(self):
        
        if not self.name or not self.name.strip():
            raise BusinessNotFoundError(self.name, "El nombre no puede estar vacío.")

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False
        
    