from dataclasses import dataclass
from domain.models.exceptions.business_exception import BusinessNotFoundError
import re

@dataclass(frozen=True)
class Password:
    
    hashed: str
    
    
    
    