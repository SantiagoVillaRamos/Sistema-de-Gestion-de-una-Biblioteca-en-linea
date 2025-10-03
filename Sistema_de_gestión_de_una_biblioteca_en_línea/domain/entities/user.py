from __future__ import annotations
from dataclasses import dataclass, field
from domain.value_objects.email import Email
from domain.value_objects.password import Password
import uuid

from domain.exceptions.user import UserNotFoundError

@dataclass
class User:
    
    user_id: str 
    name: str
    email: Email 
    password: Password
    is_active: bool = True
    
    def __post_init__(self):
        
        if not self.name or not self.name.strip():
            raise UserNotFoundError(self.name, "El nombre no puede estar vacío.")


    def activate(self) -> None:
        self.is_active = True


    def deactivate(self) -> None:
        self.is_active = False
        
    