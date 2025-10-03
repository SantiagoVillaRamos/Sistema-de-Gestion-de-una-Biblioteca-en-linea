from datetime import datetime, timedelta
from dataclasses import dataclass
from domain.models.exceptions.business_exception import BusinessNotFoundError

@dataclass
class DueDate:
    
    value: datetime
    
    def __post_init__(self):
        if self.value < datetime.now():
            raise BusinessNotFoundError(self.value, "La fecha de vencimiento no puede ser en el pasado.")
    