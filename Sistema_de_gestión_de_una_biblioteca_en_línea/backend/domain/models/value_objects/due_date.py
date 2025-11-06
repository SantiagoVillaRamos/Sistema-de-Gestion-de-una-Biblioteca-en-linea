from datetime import datetime
from dataclasses import dataclass
from domain.models.exceptions.business_exception import BusinessNotFoundError

@dataclass
class DueDate:
    
    value: datetime
    
    def __post_init__(self):
        # La comparación debe hacerse con la hora actual en la misma zona horaria
        now_aware = datetime.now(self.value.tzinfo)
        if self.value < now_aware:
            raise BusinessNotFoundError(self.value, "La fecha de vencimiento no puede ser en el pasado.")
    
    