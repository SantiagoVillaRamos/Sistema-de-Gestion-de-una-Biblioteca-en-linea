

class ResourceConflictError(Exception):
    """Excepcion base para cuando hay un conflicto (ej. recurso ya existe)."""
    pass

class ResourceNotFoundError(Exception):
    """Excepcion base para cuando un recurso no es encontrado."""
    pass

