from typing import Dict, Optional
from application.ports.user_repository import UserRepository
from domain.models.user import User
from infrastructure.mapper_infrastructure.user_mapper import UserMapper
from domain.models.exceptions.business_exception import BusinessConflictError, BusinessNotFoundError, BusinessUnauthorizedError

class UserInMemoryRepository(UserRepository):
    
    def __init__(self):
        # Ahora almacenamos diccionarios, simulando una fila de base de datos.
        self._users: Dict[str, dict] = {}
        print(f"\nDiccionario:{self._users}\n")
        
    async def save(self, user: User) -> None:
        # Usamos el mapper para obtener el email para la comprobación
        user_exists = any(u['email'] == user.email.address for u in self._users.values())
        if user_exists:
            raise BusinessConflictError(user.email.address, "El usuario con este email ya existe")
        
        # Usamos el mapper para convertir el objeto de dominio a un diccionario antes de guardarlo.
        persistence_data = UserMapper.to_persistence(user)
        self._users[user.user_id] = persistence_data


    async def find_by_id(self, user_id: str) -> Optional[User]:
        persistence_data = self._users.get(user_id)
        if not persistence_data:
            raise BusinessNotFoundError(user_id, "Usuario no encontrado")
        return UserMapper.to_domain(persistence_data)


    async def find_by_email(self, email: str) -> Optional[User]:
        for user_data in self._users.values():
            if user_data['email'] == email:
                return UserMapper.to_domain(user_data)
        return None
    
      
    async def find_all(self) -> list[User]:
        users = [ UserMapper.to_domain(user_data) for user_data in self._users.values() ]
        return users
    
    async def delete(self, user: User) -> None:
        if user.user_id not in self._users:
            raise BusinessNotFoundError(user.user_id, "No se puede eliminar un usuario que no existe.")
        del self._users[user.user_id]
   
    async def find_by_ids(self, user_ids: list[str]) -> list[User]:
        found_users = [ UserMapper.to_domain(self._users[user_id]) for user_id in user_ids if user_id in self._users ]
        return found_users
        