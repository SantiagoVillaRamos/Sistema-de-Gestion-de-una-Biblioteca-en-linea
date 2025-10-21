from fastapi import Depends, HTTPException, status, Path
from typing import Annotated
from infrastructure.web.dependencie import get_optional_current_user, get_current_user
from infrastructure.web.model.user_models import CreateUserRequest
from domain.models.user import User 

async def validate_admin_creation(
    request: CreateUserRequest,
    current_user: Annotated[User | None, Depends(get_optional_current_user)]
) -> None:
    """Verifica si el usuario autenticado tiene permiso para crear un usuario ADMIN."""
    
    is_creating_admin = "ADMIN" in (request.roles or [])
    
    # Regla: Si se está creando un admin Y hay un usuario logueado 
    # Y ese usuario logueado NO es un admin:
    if is_creating_admin and current_user and "ADMIN" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only authenticated administrators can create other administrators."
        )
        
    return None


async def validate_user_access(
    user_id: Annotated[str, Path(...)],  # Obtener el user_id de la ruta
    current_user: Annotated[User, Depends(get_current_user)], # Obtener el usuario autenticado (NO opcional)
) -> None:
    """
    Verifica si el usuario autenticado tiene permiso para ver los detalles de user_id.
    Permite: 1. ADMINS. 2. El propio usuario.
    """
    
    # 1. Verificar si el usuario actual es un ADMIN
    is_admin = "ADMIN" in current_user.roles
    
    # 2. Verificar si el usuario actual está pidiendo SUS propios datos
    is_self = current_user.user_id == user_id
    
    # Si NO es administrador Y NO es el propio usuario, denegar el acceso.
    if not is_admin and not is_self:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No autorizado para acceder a este recurso de usuario. Acceso denegado."
        )
    
    return None