from . resource import ResourceNotFoundError, ResourceConflictError, ResourceUnauthorizedError, InvalidUserTypeException

class BusinessNotFoundError(ResourceNotFoundError):
    
    def __init__(self, business_id: str, message: str):
        super().__init__(f"'{business_id}': {message}.")
        
        
class BusinessConflictError(ResourceConflictError):
    
    def __init__(self, business_id: str, message: str):
        super().__init__(f"'{business_id}': {message}.")


class BusinessUnauthorizedError(ResourceUnauthorizedError):
    def __init__(self, message: str):
        super().__init__(message)
        
        
class BusinessTypeError(InvalidUserTypeException):
    
    def __init__(self, message: str):
        super().__init__(message)