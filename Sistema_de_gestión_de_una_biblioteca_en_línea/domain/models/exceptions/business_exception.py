from . resource import ResourceNotFoundError, ResourceConflictError

class BusinessNotFoundError(ResourceNotFoundError):
    
    def __init__(self, business_id: str, message: str):
        super().__init__(f"'{business_id}': {message}.")
        
        
class BusinessConflictError(ResourceConflictError):
    
    def __init__(self, business_id: str, message: str):
        super().__init__(f"'{business_id}': {message}.")
        
        
