

class ResourceConflictError(Exception):
    """Excepcion base para cuando hay un conflicto (ej. recurso ya existe)."""
    pass

class ResourceNotFoundError(Exception):
    """Excepcion base para cuando un recurso no es encontrado."""
    pass

class ResourceUnauthorizedError(Exception):
    """Excepción base para cuando una acción no está autorizada."""
    pass

class InvalidUserTypeException(Exception):
    pass

class ResorceError(Exception):
    """Excepcion base para errores relacionados con recursos."""
    pass