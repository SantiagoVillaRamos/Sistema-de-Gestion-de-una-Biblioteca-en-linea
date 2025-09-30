from datetime import datetime, timedelta
from dataclasses import dataclass
from domain.exceptions.loan import LoanNotFoundException

@dataclass
class DueDate:
    
    value: datetime
    
    def __post_init__(self):
        if self.value < datetime.now():
            raise LoanNotFoundException(self.value, "La fecha de vencimiento no puede ser en el pasado.")
    