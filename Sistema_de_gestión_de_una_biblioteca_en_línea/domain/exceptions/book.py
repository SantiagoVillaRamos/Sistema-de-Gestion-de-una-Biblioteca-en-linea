from domain.exceptions.resource import ResourceNotFoundError, ResourceConflictError


class BookAlreadyExistsError(ResourceConflictError):
    """Excepcion lanzada cuando ocurre un error al crear un libro."""
    def __init__(self, book_id: str ):
        super().__init__(f"El libro con isbn '{book_id}' ya existe.")
        

class BookNotFoundError(ResourceNotFoundError):
    """Excepcion lanzada cuando un libro no es encontrado."""
    def __init__(self, book_id: str, message: str):
        super().__init__(f"'{book_id}':{message}.")
        
