from domain.exceptions.resource import ResourceNotFoundError, ResourceConflictError


class LoanNotFoundException(ResourceNotFoundError):
    """Excepción lanzada cuando un préstamo no es encontrado."""
    def __init__(self, loan_id: str, message:str):
        super().__init__(f" - '{loan_id}': {message}")
        
        
class LoanAlreadyReturnedException(ResourceConflictError):
    """Excepción lanzada cuando se intenta devolver un préstamo ya existente."""
    def __init__(self, loan_id: str, message: str):
        super().__init__(f"- '{loan_id}': {message}")
        

        
