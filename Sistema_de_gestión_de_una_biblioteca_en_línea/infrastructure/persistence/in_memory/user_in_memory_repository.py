from typing import Dict, Optional
from application.ports.user_repository import UserRepository
from domain.models.user import User
from infrastructure.mapper_infrastructure.user_mapper import UserMapper

from domain.models.exceptions.business_exception import BusinessConflictError, BusinessNotFoundError

class UserInMemoryRepository(UserRepository):
    
    def __init__(self):
        # Ahora almacenamos diccionarios, simulando una fila de base de datos.
        self._users: Dict[str, dict] = {}
        print(f"\nDiccionario:{self._users}\n")
        
    async def save(self, user: User) -> None:
        # Usamos el mapper para obtener el email para la comprobación
        user_exists = any(u['email'] == user.email.address for u in self._users.values())
        if user_exists:
            raise BusinessConflictError(user.email, "El usuario con este email ya existe")
        
        # Usamos el mapper para convertir el objeto de dominio a un diccionario antes de guardarlo.
        persistence_data = UserMapper.to_persistence(user)
        self._users[user.user_id] = persistence_data

    async def find_by_id(self, user_id: str) -> Optional[User]:
        persistence_data = self._users.get(user_id)
        if not persistence_data:
            raise BusinessNotFoundError(user_id, "Usuario no encontrado")
        
        # Usamos el mapper para convertir el diccionario de vuelta a un objeto de dominio.
        return UserMapper.to_domain(persistence_data)

    async def find_by_email(self, email: str) -> Optional[User]:
        for user_data in self._users.values():
            if user_data['email'] == email:
                # Usamos el mapper para convertir el diccionario de vuelta a un objeto de dominio.
                return UserMapper.to_domain(user_data)
        return None
        
        