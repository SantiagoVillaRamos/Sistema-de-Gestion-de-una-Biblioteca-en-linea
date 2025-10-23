from fastapi import Depends, HTTPException, status, Path
from typing import Annotated
from infrastructure.web.dependencie import get_optional_current_user, get_current_user
from infrastructure.web.model.user_models import UserResponse
from domain.models.user import User 


async def validate_admin_creation(
    request: UserResponse,
    current_user: Annotated[User | None, Depends(get_optional_current_user)]
) -> None:
    """Verifica si el usuario autenticado tiene permiso para crear un usuario ADMIN."""
    
    is_creating_admin = "ADMIN" in (request.roles or [])
    
    # Regla: Si se está creando un admin Y hay un usuario logueado 
    # Y ese usuario logueado NO es un admin:
    if is_creating_admin and current_user and "ADMIN" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden crear usuarios con rol ADMIN."
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


async def validate_admin_only(
    current_user: Annotated[User, Depends(get_current_user)], # Asumimos que get_current_user fuerza la autenticación
) -> None:
    """Verifica si el usuario autenticado tiene el rol ADMIN."""
    
    if "ADMIN" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requiere rol de administrador."
        )
    return None


async def validate_admin_delete(
    target_user_id: Annotated[str, Path(alias="user_id")], # ID del usuario a eliminar
    current_user: Annotated[User, Depends(get_current_user)], # Usuario que hace la petición
) -> None:
    """Verifica si el usuario autenticado es un ADMIN y no está intentando eliminarse a sí mismo."""
    
    # 1. Verificar si el usuario actual es un ADMIN
    if "ADMIN" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requiere rol de administrador para eliminar usuarios."
        )

    # 2. Verificar la regla de auto-eliminación
    if current_user.user_id == target_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un administrador no puede eliminarse a sí mismo."
        )
        
    return None