from typing import Dict, Optional
from application.ports.user_repository import UserRepository
from domain.models.user import User

from domain.models.exceptions.business_exception import BusinessConflictError, BusinessNotFoundError

class UserInMemoryRepository(UserRepository):
    
    def __init__(self):
        self._users: Dict[str, User] = {}
        print(f"\nDiccionario:{self._users}\n")
        
    async def save(self, user: User) -> None:
        user_exists = any(b for b in self._users.values() if b.email == user.email)
        if user_exists:
            raise BusinessConflictError(user.email, "El usuario con este email ya existe")
        self._users[user.user_id] = user

    async def find_by_id(self, user_id: str) -> Optional[User]:
        user = self._users.get(user_id)
        if not user:
            raise BusinessNotFoundError(user_id, "Usuario no encontrado")
        return user
        