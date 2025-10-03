from . resource import ResourceNotFoundError, ResourceConflictError

class BusinessNotFoundError(ResourceNotFoundError):
    """Excepción lanzada cuando una entidad de negocio no es encontrada."""
    def __init__(self, business_id: str, message: str):
        super().__init__(f"'{business_id}': {message}.")
        
        
class BusinessConflictError(ResourceConflictError):
    """Excepción lanzada cuando hay un conflicto en una entidad de negocio."""
    def __init__(self, business_id: str, message: str):
        super().__init__(f"'{business_id}': {message}.")