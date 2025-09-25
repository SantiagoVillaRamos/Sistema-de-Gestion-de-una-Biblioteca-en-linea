from domain.exceptions.resource import ResourceNotFoundError, ResourceConflictError


class UserAlreadyExistsError(ResourceConflictError):
    """Excepción lanzada cuando hay un error al crear un usuario."""
    def __init__(self, user_id: str):
        super().__init__(f"Error al crear el usuario: {user_id}")
       
        
class UserNotFoundError(ResourceNotFoundError):
    """Excepción lanzada cuando un usuario no es encontrado."""
    def __init__(self, value: str, message:str):
        super().__init__(f"-'{value}': {message}")



